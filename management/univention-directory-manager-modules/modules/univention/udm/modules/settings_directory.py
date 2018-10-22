# -*- coding: utf-8 -*-
#
# Copyright 2018 Univention GmbH
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
# you and Univention.
#
# This program is provided in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License with the Debian GNU/Linux or Univention distribution in file
# /usr/share/common-licenses/AGPL-3; if not, see
# <http://www.gnu.org/licenses/>.

"""
Module and object specific for "settings/directory" UDM module.
"""

from __future__ import absolute_import, unicode_literals
from ..encoders import dn_list_property_encoder_for
from .generic import GenericUdmModule, GenericUdmObject, GenericUdmObjectProperties


class SettingsDirectoryUdmObjectProperties(GenericUdmObjectProperties):
	"""settings/directory UDM properties."""

	_encoders = {
		'computers': dn_list_property_encoder_for('container/cn'),
		'dhcp': dn_list_property_encoder_for('container/cn'),
		'dns': dn_list_property_encoder_for('container/cn'),
		'groups': dn_list_property_encoder_for('container/cn'),
		'license': dn_list_property_encoder_for('container/cn'),
		'mail': dn_list_property_encoder_for('container/cn'),
		'networks': dn_list_property_encoder_for('container/cn'),
		'policies': dn_list_property_encoder_for('auto'),
		'printers': dn_list_property_encoder_for('container/cn'),
		'shares': dn_list_property_encoder_for('container/cn'),
		'users': dn_list_property_encoder_for('container/cn'),
	}


class SettingsDirectoryUdmObject(GenericUdmObject):
	"""Better representation of settings/directory properties."""
	udm_prop_class = SettingsDirectoryUdmObjectProperties


class SettingsDirectoryUdmModule(GenericUdmModule):
	"""SettingsDirectoryUdmObject factory"""
	_udm_object_class = SettingsDirectoryUdmObject
	supported_api_versions = (1,)
