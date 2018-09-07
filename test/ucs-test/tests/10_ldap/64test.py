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

        #Create new user
        try:
            user_helpdesk_dn,user_helpdesk_name = udm.create_user(password ='univention')
        except Exception:
            fail('Creating user failed:')
        else:
            print 'Creating user succeeded:'
                
        #Create new user
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
            fail('Creating user failed: %s' % user_unprotected_name)
        else:
            print 'Creating user succeeded: %s' % user_unprotected_name

        #Add user to corresponding group
        try:
            udm.modify_object('groups/group', dn=helpdesk_dn, append={'users': [user_helpdesk_dn]})
        except:
            fail('Adding user to corresponding group failed: %s in %s ' %(helpdeskname,user_helpdesk_name))
        else:
            print 'Adding user to corresponding group successful'

        ## Allow users to modify their password in Univention Directory Manager
        ucr_test["ldap/acl/user/password/change"]="yes"
        ucr_test["ldap/acl/user/passwordreset/accesslist/groups/dn"] = helpdesk_dn
        ucr_test["ldap/acl/user/passwordreset/protected/uid"] = "Administrator,%s" % (user_protected_name,)

        ## Activate passwordreset ACLs:
        cmd=["/etc/init.d/slapd", "crestart"]
        p1 = subprocess.Popen(cmd, close_fds=True)
        (stdout, stderr) = p1.communicate()
        if p1.returncode != 0:
            fail('Restarting slapd failed: %s' % stderr)
        
        #Check if Administrator can set it's own password
        try:
            udm.modify_object('users/user',binnddn=user_helpdesk_dn, bindpwd = 'univention', dn=user_helpdesk_dn, password=uts.random_string())
        except:
            fail('Administrator can not set his own password')
        else:
            print 'Administrator changed his password successfully'
        
        #Check if protected user can set his own password
        try:
            udm.modify_object('users/user', binddn =user_protected_dn, bindpwd ='univention', dn = user_protected_dn , password = uts.random_string())
        except:
            fail('Protected user %s can not set his own password' %(user_protected_name))
        else:
            print 'Protected user %s changed his password successfully' %(user_protected_name)

        #Check if unprotected user can set his own password
        try:
            udm.modify_object('users/user', binddn = user_unprotected_dn, bindpwd = 'univention' , dn =user_unprotected_dn, password = uts.random_string())
        except:
            fail('Unprotected usre %s can not set his own password'%(user_unprotected_name))
        else:
            print 'Unprotected user %s changed his password successfully' %(user_unprotected_name)


# vim: set ft=python ts=7 noexpandtab :
