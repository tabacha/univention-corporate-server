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
Module and object specific for "settings/portal" UDM module.
"""

from __future__ import absolute_import, unicode_literals
from ..encoders import (
	dn_list_property_encoder_for, Base64BinaryPropertyEncoder, StringCaseInsensitiveResultUpperBooleanPropertyEncoder,
	ListOfListOflTextToDictPropertyEncoder,
)
from .generic import GenericUdmModule, GenericUdmObject, GenericUdmObjectProperties


class SettingsPortalUdmObjectProperties(GenericUdmObjectProperties):
	"""settings/portal UDM properties."""

	_encoders = {
		'background': Base64BinaryPropertyEncoder,
		'displayName': ListOfListOflTextToDictPropertyEncoder,
		'logo': Base64BinaryPropertyEncoder,
		'portalComputers': dn_list_property_encoder_for('auto'),  # can be different types of computer/* objects
		'portalEntriesOrder': dn_list_property_encoder_for('settings/portal_entry'),  # not really sure about this as it's not exposed through the cli or python frontend, guessed it from the syntax
		'showApps': StringCaseInsensitiveResultUpperBooleanPropertyEncoder,
		'showLogin': StringCaseInsensitiveResultUpperBooleanPropertyEncoder,
		'showMenu': StringCaseInsensitiveResultUpperBooleanPropertyEncoder,
		'showSearch': StringCaseInsensitiveResultUpperBooleanPropertyEncoder,
		'showServers': StringCaseInsensitiveResultUpperBooleanPropertyEncoder,
	}


class SettingsPortalUdmObject(GenericUdmObject):
	"""Better representation of settings/portal properties."""
	udm_prop_class = SettingsPortalUdmObjectProperties


class SettingsPortalUdmModule(GenericUdmModule):
	"""SettingsPortalUdmObject factory"""
	_udm_object_class = SettingsPortalUdmObject
	supported_api_versions = (1,)
