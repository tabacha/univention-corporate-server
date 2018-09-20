#!/usr/share/ucs-test/runner python2.7
## desc: Tests functionality of nested groups
## roles-not:
##  - basesystem
## packages:
##  - python-univention-lib
## exposure: safe

from univention.testing.debian_package import DebianPackage
from univention.testing.utils import fail
# from univention.config_registry import ConfigRegistry
import subprocess
from univention.testing.ucr import UCSTestConfigRegistry
from univention.testing.udm import UCSTestUDM
import univention.testing.strings as uts


with UCSTestConfigRegistry() as ucr_test:
	ucr_test.load()
	ucr_test["apache2/documentroot"] = "/var/tmp"

	print "DEBUG2", ucr_test["apache2/documentroot"]


	with UCSTestUDM() as udm:
        
		 #Create new helpdesk group
		try:
			helpdesk_dn, helpdeskname  = udm.create_group()
		except Exception:
			print 'cant create %s' %helpdeskname    
		else:
			print 'created %s' %helpdeskname

		#Create new helpdesk user
		try:
			user_helpdesk_dn,user_helpdesk_name = udm.create_user(password ='univention')
		except Exception:
			fail('Creating user failed:')
		else:
			print 'Creating user succeeded:'

		#Create new helpdesk user
		try:
			user2_helpdesk_dn,user2_helpdesk_name = udm.create_user(password ='univention')
		except Exception:
			fail('Creating user failed:')
		else:
			print 'Creating user succeeded:'

		#Create new protected user
		try:
			user_protected_dn, user_protected_name = udm.create_user(password = 'univention')
		except Exception:
			fail('Creating user failed: %s' % user_protected_name)
		else:
			print 'Creating user succeeded: %s' % user_protected_name
        
		#Create new unprotected user
		try:
			user_unprotected_dn, user_unprotected_name = udm.create_user(password = 'univention')
		except Exception:
			fail('Creating user failed %s ' %user_unprotected_name)
		else:
			print 'Creating user succeeded : %s' %user_unprotected_name

		#Add helpdesk user to helpdesk group
		try:
			udm.modify_object('groups/group', dn=helpdesk_dn, append={'users': [user_helpdesk_dn]})
		except Exception:
			fail('Adding user to corresponding group failed: %s in %s ' %(helpdeskname,user_helpdesk_name))
		else:
			print 'Adding user to corresponding group successful'

		#Create second helpdesk group
		try:
			helpdesk2_dn,helpdesk2_name= udm.create_group()
		except Exception:
			fail('Cant create %s ' %helpdesk2_name)
		else:
			print 'created  %s' %helpdesk2_name
        
		#Add second helpdesk user to second helpdesk group
		try:
			udm.modify_object('groups/group', dn = helpdesk2_dn, append ={'users' : [user2_helpdesk_dn]})
		except Exception:
			fail('Can not add %s to %s ' %(user2_helpdesk_name, helpdesk2_name))
		else:
			print 'successfully added %s to %s ' %(user2_helpdesk_name, helpdesk2_name)
        
		#Create nested group
		try:
			udm.modify_object('groups/group', dn = helpdesk_dn, append = {'nestedGroup':[helpdesk2_dn]})
		except Exception:
			fail('Cant create nested group')
		else:
			print 'created nested group'

		## Allow users to modify their password in Univention Directory Manager
		ucr_test["ldap/acl/user/passwordreset/accesslist/groups/dn"] = helpdesk_dn
		ucr_test["ldap/acl/user/passwordreset/protected/uid"] = "Administrator,%s" % (user_protected_name,)
		ucr_test['ldap/acl/nestedgroups']='no'

		## Activate passwordreset ACLs:
		cmd=["/etc/init.d/slapd", "crestart"]
		p1 = subprocess.Popen(cmd, close_fds=True)
		(stdout, stderr) = p1.communicate()
		if p1.returncode != 0:
			fail('Restarting slapd failed: %s' % stderr)

		#Test if Helpdesk user can reset password of unprotected user
		try:
			udm.modify_object('users/user', binddn = user_helpdesk_dn, bindpw = 'univention', dn= user_unprotected_dn, password = uts.random_string())
		except Exception:
			fail('helpdesk user cant reset password of unprotected user')
		else:
			print 'helpdesk user resetted password of unprotected user successfully'
        
		#Test if nested helpdesk user can reset password of unprotected user  
		try:
			udm.modify_object('users/user', binddn = user2_helpdesk_dn, bindpw = 'univention', dn= user_unprotected_dn, password = uts.random_string())
		except Exception:
			fail('Nested helpdesk user can reset password of unprotected user, but should not be able to')
			pass
		else: 
			print 'nested helpdesk user can not reset password of unprotected user, as it should be'
        

		#Enable nested group tests
		ucr_test['dap/acl/nestedgroups']='yes'

		#Test if helpdesk user can still reset password of unprotected user
		try:
			udm.modify_object('users/user', binddn = user_helpdesk_dn, bindpw = 'univention', dn = user_unprotected_dn , password = uts.random_string())
		except Exception:
			fail('Helpdesk user can not set password of unprotected user')
		else:
			print 'Helpdesk user set password of unprotected user successfully'
      

		#Test if nested helpdesk user can reset password of unprotected user
		try:
			udm.modify_object('users/user', binddn = user2_helpdesk_dn, bindpw = 'univention', dn = user_unprotected_dn, password = uts.random_string())
		except Exception:
			fail('nested helpdesk user can not reset password of unprotected user')
		else:
			print 'nested helpdesk user set password of unprotected user successfully'



# vim: set ft=python ts=7 noexpandtab :
