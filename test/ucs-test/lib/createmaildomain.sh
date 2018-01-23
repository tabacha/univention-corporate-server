#!/bin/bash
CONTROLMODE=true
. "$TESTLIBPATH/base.sh" || exit 137
. "$TESTLIBPATH/random.sh" || exit 137

maildomain_name_randomname () { #Generates a random string as maildomain an echoes it. Usage: MAILDOMAINNAME=$(maildomain_name_randomname)
        random_string
}


create_mail_domain () { #Creates a mail/domain name like the first argument, supplied to the function.
	# creating a mail/domain name could be like:
	# MAILDOMAINNAME=$(maildomain_name_randomname)
	# create_mail_domain "$MAILDOMAINNAME"

		if [ -z "$1" ]
		then
			echo "No mail/domain name has been supplied.\n"
			echo "You have to supply a mail/domain name e.g. generated by \$(maildomain_name_randomname)"
			return 1
		else
			udm mail/domain create --set name="$1"
			# udm command should be the last statement within function
		fi

}

delete_mail_domain () { # Deletes a mail/domain name like the first argument, supplied to the function.
	# creating a mail/domain name could be like:
	# MAILDOMAINNAME=$(maildomain_name_randomname)
	# create_mail_domain "$MAILDOMAINNAME"

		if [ -z "$1" ]
		then
			echo "No mail/domain name has been supplied to delete.\n"
			echo "You have to supply a mail/domain name e.g. generated by \$(maildomain_name_randomname)"
			return 1
		else
			udm mail/domain remove --dn "cn=$1,$ldap_base"
			# udm command should be the last statement within function
		fi
}