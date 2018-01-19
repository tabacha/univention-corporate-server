# -*- coding: utf-8 -*-
#
# Univention Admin Modules
#  unit tests: policies/dhcp_scope tests
#
# Copyright 2004-2016 Univention GmbH
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


from GenericTest import GenericTestCase


class PolicyDhcpScopeTestCase(GenericTestCase):

	def __init__(self, *args, **kwargs):
		self.modname = 'policies/dhcp_scope'
		super(PolicyDhcpScopeTestCase,
		      self).__init__(*args, **kwargs)

	def setUp(self):
		super(PolicyDhcpScopeTestCase, self).setUp()
		self.createProperties = {
			'requiredObjectClasses': 'univentionHost',
			'prohibitedObjectClasses': 'posixAccount',
			'fixedAttributes': 'univentionDhcpBootp',
			'bootp': 'allow',
			'declines': 'deny',
			'duplicates': 'allow',
			'booting': 'deny',
			'scopeUnknownClients': 'deny',
		}
		self.modifyProperties = {
			'requiredObjectClasses': 'posixAccount',
			'prohibitedObjectClasses': 'univentionHost',
			'fixedAttributes': 'univentionDhcpBooting',
			'bootp': 'deny',
			'declines': 'allow',
			'duplicates': 'deny',
			'booting': 'allow',
			'scopeUnknownClients': 'allow',
		}
		self.name = 'testdhcpscopepolicy'


def suite():

	import unittest
	suite = unittest.TestSuite()
	suite.addTest(PolicyDhcpScopeTestCase())
	return suite


if __name__ == '__main__':
	import unittest
	unittest.TextTestRunner().run(suite())