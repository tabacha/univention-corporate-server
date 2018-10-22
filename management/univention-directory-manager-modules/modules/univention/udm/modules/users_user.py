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
Module and object specific for "users/user" UDM module.
"""

from __future__ import absolute_import, unicode_literals
from ..encoders import (
	dn_list_property_encoder_for, dn_property_encoder_for, Base64BinaryPropertyEncoder, DatePropertyEncoder,
	DisabledPropertyEncoder, HomePostalAddressPropertyEncoder, SambaLogonHoursPropertyEncoder, StringIntPropertyEncoder,
)
from ..exceptions import NoObject
from .generic import GenericUdmModule, GenericUdmObject, GenericUdmObjectProperties


class UsersUserUdmObjectProperties(GenericUdmObjectProperties):
	"""users/user UDM properties."""

	_encoders = {
		'birthday': DatePropertyEncoder,
		'disabled': DisabledPropertyEncoder,
		'gidNumber': StringIntPropertyEncoder,
		'groups': dn_list_property_encoder_for('groups/group'),
		'homePostalAddress': HomePostalAddressPropertyEncoder,
		'jpegPhoto': Base64BinaryPropertyEncoder,
		'mailForwardCopyToSelf': DisabledPropertyEncoder,
		'mailUserQuota': StringIntPropertyEncoder,
		'primaryGroup': dn_property_encoder_for('groups/group'),
		'sambaLogonHours': SambaLogonHoursPropertyEncoder,
		'sambaRID': StringIntPropertyEncoder,
		'secretary': dn_list_property_encoder_for('users/user'),
		'serviceprovider': dn_list_property_encoder_for('saml/serviceprovider'),
		'uidNumber': StringIntPropertyEncoder,
		'userexpiry': DatePropertyEncoder,
	}


class UsersUserUdmObject(GenericUdmObject):
	"""Better representation of users/user properties."""
	udm_prop_class = UsersUserUdmObjectProperties


class UsersUserUdmModule(GenericUdmModule):
	"""UsersUserUdmObject factory"""
	_udm_object_class = UsersUserUdmObject
	supported_api_versions = (1,)

	def _get_default_positions_property(self):
		return 'users'
