#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
#
# Univention Debmirror
#  mirrors a repository server
#
# Copyright 2009-2018 Univention GmbH
#
# http://www.univention.de/
#
# All rights reserved.
#
# The source code of this program is made available
# under the terms of the GNU Affero General Public License version 3
# (GNU AGPL V3) as published by the Free Software Foundation.
#
# Binary versions of this program provided by Univention to you as
# well as other copyrighted, protected or trademarked materials like
# Logos, graphics, fonts, specific documentations and configurations,
# cryptographic keys etc. are subject to a license agreement between
# you and Univention and not subject to the GNU AGPL V3.
#
# In the case you use this program under the terms of the GNU AGPL V3,
# the program is provided in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License with the Debian GNU/Linux or Univention distribution in file
# /usr/share/common-licenses/AGPL-3; if not, see
# <http://www.gnu.org/licenses/>.

import os
import errno
import re
import subprocess
import itertools
import logging
from operator import itemgetter

from tools import UniventionUpdater, NullHandler
from ucs_version import UCS_Version
from repo_url import UcsRepoUrl
try:
    import univention.debug as ud
except ImportError:
    import univention.debug2 as ud


def makedirs(dirname, mode=0o755):
    try:
        os.makedirs(dirname, mode)
    except OSError as ex:
        if ex.errno != errno.EEXIST:
            raise


class UniventionMirror(UniventionUpdater):

    def __init__(self, check_access=True):
        UniventionUpdater.__init__(self, check_access)
        self.log = logging.getLogger('updater.Mirror')
        self.log.addHandler(NullHandler())
        self.repository_path = self.configRegistry.get('repository/mirror/basepath', '/var/lib/univention-repository')

        version_end = self.configRegistry.get('repository/mirror/version/end') or self.current_version
        self.version_end = UCS_Version(version_end)
        version_start = self.configRegistry.get('repository/mirror/version/start') or (self.version_major, 0, 0)
        self.version_start = UCS_Version(version_start)
        # set architectures to mirror
        archs = self.configRegistry.get('repository/mirror/architectures', '')
        if archs:
            self.architectures = archs.split(' ')

    def config_repository(self):
        """ Retrieve configuration to access repository. Overrides UniventionUpdater. """
        self.online_repository = self.configRegistry.is_true('repository/mirror', True)
        self.repourl = UcsRepoUrl(self.configRegistry, 'repository/mirror')
        self.sources = self.configRegistry.is_true('repository/mirror/sources', False)
        self.timeout = float(self.configRegistry.get('repository/mirror/timeout', 30))
        self.http_method = self.configRegistry.get('repository/mirror/httpmethod', 'HEAD').upper()
        self.script_verify = self.configRegistry.is_true('repository/mirror/verify', True)

    def release_update_available(self, ucs_version=None, errorsto='stderr'):
        '''Check if an update is available for the ucs_version'''
        if not ucs_version:
            ucs_version = self.current_version
        return self.get_next_version(UCS_Version(ucs_version), [], errorsto)

    def mirror_repositories(self):
        '''uses apt-mirror to copy a repository'''
        # check if the repository directory structure exists, otherwise create it
        makedirs(self.repository_path)

        # these sub-directories are required by apt-mirror
        for dir in ('skel', 'mirror', 'var'):
            path = os.path.join(self.repository_path, dir)
            makedirs(path)
        path = os.path.join(self.repository_path, 'mirror', 'univention-repository')
        try:
            os.symlink('.', path)
        except OSError as ex:
            if ex.errno != errno.EEXIST:
                raise

        log = open('/var/log/univention/repository.log', 'a')
        try:
            return subprocess.call('/usr/bin/apt-mirror', stdout=log, stderr=log, shell=False)
        finally:
            log.close()

    def mirror_update_scripts(self):
        '''mirrors the preup.sh and postup.sh scripts'''
        start = self.version_start
        end = self.version_end
        parts = self.parts
        archs = ('all',)

        repos = self._iterate_version_repositories(start, end, parts, archs)  # returns generator

        start_errata = UCS_Version((start.major, start.minor, 1))  # errata updates start with 'errata1'
        end_errata = UCS_Version((end.major, end.minor, 999))  # get all available for mirror
        errata = self._iterate_errata_repositories(start_errata, end_errata, parts, archs)  # returns generator

        components = self.get_components(only_localmirror_enabled=True)
        comp = self._iterate_component_repositories(components, start, end, archs, for_mirror_list=True)  # returns generator

        all_repos = itertools.chain(repos, errata, comp)  # concatenate all generators into a single one
        for server, struct, phase, path, script in UniventionUpdater.get_sh_files(all_repos, self.script_verify):
            self.log.info('Mirroring %s:%r/%s to %s', server, struct, phase, path)
            assert script is not None, 'No script'

            # use prefix if defined - otherwise file will be stored in wrong directory
            if server.prefix:
                filename = os.path.join(self.repository_path, 'mirror', server.prefix, path)
            else:
                filename = os.path.join(self.repository_path, 'mirror', path)

            # Check disabled, otherwise files won't get refetched if they change on upstream server
            # if os.path.exists(filename):
            #   ud.debug(ud.NETWORK, ud.ALL, "Script already exists, skipping: %s" % filename)
            #   continue

            makedirs(os.path.dirname(filename))
            fd = open(filename, "w")
            try:
                fd.write(script)
                ud.debug(ud.ADMIN, ud.INFO, "Successfully mirrored: %s" % filename)
            finally:
                fd.close()

    def list_local_repositories(self, start=None, end=None, maintained=True, unmaintained=False):
        '''
        This function returns a sorted list of local (un)maintained repositories.
        Arguments: start: smallest version that shall be returned (type: UCS_Version)
                           end:   largest version that shall be returned (type: UCS_Version)
                           maintained:   True if list shall contain maintained repositories
                           unmaintained: True if list shall contain unmaintained repositories
        Returns: a list of ( directory, UCS_Version, is_maintained ) tuples.
        '''
        result = []
        repobase = os.path.join(self.repository_path, 'mirror')
        RErepo = re.compile('^%s/(\d+[.]\d)/(maintained|unmaintained)/(\d+[.]\d+-\d+)$' % (re.escape(repobase),))
        for dirname, subdirs, files in os.walk(repobase):
            match = RErepo.match(dirname)
            if match:
                if not maintained and match.group(2) == 'maintained':
                    continue
                if not unmaintained and match.group(2) == 'unmaintained':
                    continue

                version = UCS_Version(match.group(3))
                if start is not None and version < start:
                    continue
                if end is not None and end < version:
                    continue

                result.append((dirname, version, match.group(2) == 'maintained'))

        result.sort(key=itemgetter(1))

        return result

    def run(self):
        '''starts the mirror process'''
        self.mirror_repositories()
        self.mirror_update_scripts()


if __name__ == '__main__':
    import doctest
    from sys import exit
    exit(doctest.testmod()[0])
