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
TEST module and object specific for "users/user" UDM module.
"""

from __future__ import absolute_import
from .generic import GenericUdm1Module, GenericUdm1Object

try:
	from typing import Dict, List, Text
except ImportError:
	pass


class UsersUserUdm1Object(GenericUdm1Object):
	"""Test dynamic factory"""

	def _decode_prop_homePostalAddress(self, value):  # type: (List[List[Text]]) -> List[Dict[str, Text]]
		return [{'street': v[0], 'zipcode': v[1], 'city': v[2]} for v in value]

	def _encode_prop_homePostalAddress(self, value):  # type: (List[Dict[str, Text]]) -> List[List[Text]]
		return [[v['street'], v['zipcode'], v['city']] for v in value]


class UsersUserUdm1Module(GenericUdm1Module):
	"""Test dynamic factory"""
	_udm_object_class = UsersUserUdm1Object
