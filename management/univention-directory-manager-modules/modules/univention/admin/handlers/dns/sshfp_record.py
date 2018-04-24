# -*- coding: utf-8 -*-
# Univention Admin Modules for DNS SSH finger print records
#
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright 2004-2018 Univention GmbH
# <https://tools.ietf.org/html/rfc4255>
# <https://tools.ietf.org/html/rfc6594>
# <https://www.iana.org/assignments/dns-sshfp-rr-parameters/dns-sshfp-rr-parameters.xhtml>

from univention.admin.layout import Tab, Group
import univention.admin.filter
import univention.admin.handlers
import univention.admin.handlers.dns.forward_zone
import univention.admin.localization
from univention.admin.handlers.dns import unmapSSHFP, mapSSHFP

translation = univention.admin.localization.translation('univention.admin.handlers.dns')
_ = translation.translate

module = 'dns/sshfp_record'
operations = ['add', 'edit', 'remove', 'search']
columns = ['fingerprint']
superordinate = 'dns/forward_zone'
childs = 0
short_description = _('DNS: Secure Shell Fingerprint record')
long_description = _('Store fingerprint of Secure Shell host keys.')
options = {
	'default': univention.admin.option(
		default=True,
		objectClasses=['top', 'dNSZone'],
	),
}
property_descriptions = {
	'name': univention.admin.property(
		short_description=_('Name'),
		long_description=_('The name of the host relative to the domain.'),
		syntax=univention.admin.syntax.dnsName,
		include_in_default_search=True,
		required=True,
		identifies=True
	),
	'zonettl': univention.admin.property(
		short_description=_('Time to live'),
		long_description=_('The time this entry may be cached.'),
		syntax=univention.admin.syntax.UNIX_TimeInterval,
		required=False,
		identifies=False,
		default=(('22', 'hours'), [])
	),
	'fingerprint': univention.admin.property(
		short_description=_('SSH host key fingerprint'),
		long_description=_('Fingerprint of the Secure Shell host keys.'),
		syntax=univention.admin.syntax.dnsSSHFP,
		multivalue=True,
		required=True,
		identifies=False,
	),
}
layout = [
	Tab(_('General'), _('Basic settings'), layout=[
		Group(_('SSH host key settings'), layout=[
			'name',
			'fingerprint',
			'zonettl'
		]),
	]),
]


mapping = univention.admin.mapping.mapping()
mapping.register('name', 'relativeDomainName', None, univention.admin.mapping.ListToString)
mapping.register('fingerprint', 'sSHFPRecord', mapSSHFP, unmapSSHFP)
mapping.register('zonettl', 'dNSTTL', univention.admin.mapping.mapUNIX_TimeInterval, univention.admin.mapping.unmapUNIX_TimeInterval)


class object(univention.admin.handlers.simpleLdap):
	module = module

	def _updateZone(self):
		if self.update_zone:
			self.superordinate.open()
			self.superordinate.modify()

	def __init__(self, co, lo, position, dn='', superordinate=None, attributes=[], update_zone=True):
		self.update_zone = update_zone
		univention.admin.handlers.simpleLdap.__init__(self, co, lo, position, dn, superordinate, attributes=attributes)

	def _ldap_addlist(self):
		return [
			(self.superordinate.mapping.mapName('zone'), self.superordinate.mapping.mapValue('zone', self.superordinate['zone'])),
		]

	def _ldap_post_create(self):
		self._updateZone()

	def _ldap_post_modify(self):
		if self.hasChanged(self.descriptions.keys()):
			self._updateZone()

	def _ldap_post_remove(self):
		self._updateZone()


def lookup(co, lo, filter_s, base='', superordinate=None, scope="sub", unique=False, required=False, timeout=-1, sizelimit=0):

	filter = univention.admin.filter.conjunction('&', [
		univention.admin.filter.expression('objectClass', 'dNSZone'),
		univention.admin.filter.conjunction('!', [univention.admin.filter.expression('relativeDomainName', '@')]),
		univention.admin.filter.conjunction('!', [univention.admin.filter.expression('zoneName', '*.in-addr.arpa')]),
		univention.admin.filter.conjunction('!', [univention.admin.filter.expression('zoneName', '*.ip6.arpa')]),
		univention.admin.filter.expression('sSHFPRecord', '*'),
	])

	if superordinate:
		filter.expressions.append(univention.admin.filter.expression('zoneName', superordinate.mapping.mapValue('zone', superordinate['zone']), escape=True))

	if filter_s:
		filter_p = univention.admin.filter.parse(filter_s)
		univention.admin.filter.walk(filter_p, univention.admin.mapping.mapRewrite, arg=mapping)
		filter.expressions.append(filter_p)

	res = []
	for dn, attrs in lo.search(unicode(filter), base, scope, [], unique, required, timeout, sizelimit):
		res.append((object(co, lo, None, dn=dn, superordinate=superordinate, attributes=attrs)))
	return res


def identify(dn, attr, canonical=0):
	return all([
		'dNSZone' in attr.get('objectClass', []),
		'@' not in attr.get('relativeDomainName', []),
		not attr.get('zoneName', ['.in-addr.arpa'])[0].endswith('.in-addr.arpa'),
		not attr.get('zoneName', ['.ip6.arpa'])[0].endswith('.ip6.arpa'),
		attr.get('sSHFPRecord', [])
	])
