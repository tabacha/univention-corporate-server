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

from __future__ import unicode_literals
try:
	from typing import Iterable, Optional, Text
except ImportError:
	pass


class UdmError(Exception):
	"""Base class of Exceptions raised by (simplified) UDM modules."""
	def __init__(self, msg, dn=None, module_name=None):
		# type: (Text, Optional[Text], Optional[Text]) -> None
		super(UdmError, self).__init__(msg)
		self.dn = dn
		self.module_name = module_name


class ApiVersionNotSupported(UdmError):
	def __init__(
		self,
		msg=None,  # type: Text
		module_name=None,  # type: Text
		module_cls=None,  # type: type
		requested_version=None,  # type: int
		supported_versions=None,  # type: Iterable
	):
		#  type: (...) -> None
		self.module_cls = module_cls
		self.requested_version = requested_version
		self.supported_versions = supported_versions
		msg = msg or 'Class {!r} for module {!r} supports API versions {!r}, but {!r} was requested.'.format(
			module_cls, module_name, supported_versions, requested_version)
		super(ApiVersionNotSupported, self).__init__(msg, module_name=module_name)


class DeletedError(UdmError):
	def __init__(self, msg=None, dn=None, module_name=None):
		# type: (Optional[Text], Optional[Text], Optional[Text]) -> None
		msg = msg or 'Object{} has already been deleted.'.format(' {!r}'.format(dn) if dn else '')
		super(DeletedError, self).__init__(msg, dn, module_name)


class FirstUseError(UdmError):
	"""
	Raised when a client tries to delete or reload a UdmObject that is not yet
	saved.
	"""
	def __init__(self, msg=None, dn=None, module_name=None):
		# type: (Optional[Text], Optional[Text], Optional[Text]) -> None
		msg = msg or 'Object has not been created/loaded yet.'
		super(FirstUseError, self).__init__(msg, dn, module_name)


class ModifyError(UdmError):
	"""Raised when an error occurred when moving an object."""
	pass


class MoveError(UdmError):
	"""Raised if an error occurred when moving an object."""
	pass


class NoObject(UdmError):
	"""Raised when a UdmObject could not be found at a DN."""
	def __init__(self, msg=None, dn=None, module_name=None):
		# type: (Optional[Text], Optional[Text], Optional[Text]) -> None
		msg = msg or 'No object found at DN {!r}.'.format(dn)
		super(NoObject, self).__init__(msg, dn, module_name)


class UnknownUdmModuleType(UdmError):
	"""
	Raised when an LDAP object has no or empty attribute univentionObjectType.
	"""
	def __init__(self, msg=None, dn=None, module_name=None):
		# type: (Optional[Text], Optional[Text], Optional[Text]) -> None
		msg = msg or 'No or empty attribute "univentionObjectType" found at DN {!r}.'.format(dn)
		super(UnknownUdmModuleType, self).__init__(msg, dn, module_name)


class UnknownProperty(UdmError):
	"""
	Raised when a client tries to set a property on UdmObject.props, that it
	does not support.
	"""
	pass


class WrongObjectType(UdmError):
	"""
	Raised when the LDAP object to be loaded does not match the UdmModule type.
	"""
	def __init__(self, msg=None, dn=None, module_name=None, univention_object_type=None):
		# type: (Optional[Text], Optional[Text], Optional[Text], Optional[Text]) -> None
		msg = msg or 'Wrong UDM module: {!r} is not a {!r}, but a {!r}.'.format(dn, module_name, univention_object_type)
		super(WrongObjectType, self).__init__(msg, dn, module_name)
