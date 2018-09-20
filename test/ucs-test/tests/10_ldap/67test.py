#!/usr/share/ucs-test/runner python2.7
## desc: Test example
## roles-not:
##  - basesystem
## packages:
##  - python-univention-lib
## exposure: safe

from univention.testing.debian_package import DebianPackage
from univention.testing.utils import fail
# from univention.config_registry import ConfigRegistry

from univention.testing.ucr import UCSTestConfigRegistry
from univention.testing.udm import UCSTestUDM
import subprocess
import univention.testing.strings as uts

with UCSTestConfigRegistry() as ucr_test:
	ucr_test.load()
	ucr_test["apache2/documentroot"] = "/var/tmp"
	debug=ucr_test['ldap/base'] 
	print "DEBUG2", ucr_test["apache2/documentroot"]
	print debug
	with UCSTestUDM() as udm:

		#create user
		try:
			user_dn,user_name = udm.create_user(password='univention', groups="cn=Domain Admins,cn=groups,%s"%(ucr_test["ldap/base"]))
		except Exception:
			fail('Creating user failes: %s' %user_name)
		else:
			print 'Creating user succeeded: %s' %user_name

		#create helpdesk user
		try:
			user_helpdesk_dn, user_helpdesk_name = udm.create_user(password='univention')
		except Exception:
			fail('Creating user failed: %s' % user_helpdesk_name)
		else:
			print 'Creating user succeeded: %s' % user_helpdesk_name

		#create domain admin member
		try:
			user_domainadmin_dn, user_domainadmin_name = udm.create_user(password='univention')
		except Exception:
			fail('Creating user failed: %s' % user_domainadmin_name)
		else:
			print 'Creating user succeeded: %s' % user_domainadmin_name
		
		#create domain admin member 2
		try:
			user_domainadmin2_dn, user_domainadmin2_name =udm.create_user(password='univention')
		except Exception:
			fail('Creating user failed: %s' % user_domainadmin2_name)
		else:
			print 'Creating user succeeded: %s' % user_domainadmin2_name

		#set admin group as primary group for domain admin 2
		try:
			udm.modify_object("users/user",dn=user_domainadmin2_dn,set={'primaryGroup':["cn=Domain Admins,cn=groups,%s"%(ucr_test["ldap/base"])]})
		except Exception:
			fail('cant set the  primary group %s, to Domain Admin group'%(user_domainadmin2_dn))
		else:
			print 'set the primary group of %s to Doman Admins '%(user_domainadmin2_dn)
		
		#Set group of domain admin to domain admins
		try:
			udm.modify_object("users/user", dn=user_domainadmin_dn,set={"groups":["cn=Domain Admins,cn=groups,%s"%(ucr_test["ldap/base"])]})
		except Exception:
			fail('could not add user to the domain admin group')
		else:
			print  "Added domainadmin to domain admin group"

		#set group of helpdesk user to User Password Admins
		try:
			udm.modify_object("users/user",dn=user_helpdesk_dn,set={"groups":["cn=User Password Admins,cn=groups,%s"%(ucr_test["ldap/base"])]})
		except Exception:
			fail('could not add user to User Password Admin Group')
		else:
			print 'added helpdesk user to User Password Admin Group'
		
		#TODO:Even though the admin users should be added to the Domain Admins group, they are not in the groupmemberlist
		print "Password Accesslist Groups:              !!!!%s"%(ucr_test["ldap/acl/user/passwordreset/accesslist/groups/dn"])
		print "Password reset protected groups          !!!!%s"%(ucr_test["ldap/acl/user/passwordreset/protected/gid"])
		print "Password reset protected users           !!!!%s"%(ucr_test["ldap/acl/user/passwordreset/protected/uid"])
		print "Members of group User Password Admins    !!!!%s"%(ucr_test["ldap/acl/user/passwordreset/internal/groupmemberlist/User Password Admins"])
		print "Members of group Domain Admins           !!!!%s"%(ucr_test["ldap/acl/user/passwordreset/internal/groupmemberlist/Domain Admins"])

		#sldap restart
		## Activate passwordreset ACLs:
		cmd=["/etc/init.d/slapd", "crestart"]
		p1 = subprocess.Popen(cmd, close_fds=True)
		(stdout, stderr) = p1.communicate()
		if p1.returncode != 0:
			fail('Restarting slapd failed: %s' % stderr)

		#Test if Helpdesk user can reset password of admin 
		try:
			udm.modify_object('users/user', binddn = user_helpdesk_dn,bindpw ='univention',dn= user_domainadmin_dn, password = uts.random_string())
		except Exception:
			print 'helpdesk user cant reset password of admin user, as expected'
		else:
			fail('helpdesk user resetted password of protected user successfully')
		#FIXME everyone seems to be allowed to set passwords...
		
		#Test if Helpdesk user can reset password of admin2
		try:
			udm.modify_object('users/user', binddn = user_helpdesk_dn, bindpw ='univention', dn= user_domainadmin2_dn, password =uts.random_string())
		except Exception:
			print 'helpdesk user cant reset password of unprotected user'
		else:
			fail( 'helpdesk user resetted password of unprotected user, but should not be able to')

		#Test if Helpdesk user can reset password of user
		try:
			udm.modify_object('users/user', binddn =user_helpdesk_dn, bindpw ='univention', dn= user_dn, password =uts.random_string())
		except Exception:
			fail( 'helpdesk user cant reset password of user')
		else:
			print 'helpdesk user resetted password of user'



# vim: set ft=python ts=7 noexpandtab :
