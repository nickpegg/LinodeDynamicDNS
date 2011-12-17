#!/usr/bin/env python

# LinodeDynamicDNS.py - A dynamic DNS updater for Linode's DNS service
# By Nick Pegg (nick@nickpegg.com)
#
# Inspired by Jed Smith's dynamic DNS updater, but this one doesn't require 
# you to find any pesky ID numbers. Plus, this uses the linode-python library,
# which can be found here: https://github.com/tjfontaine/linode-python/


# You better damn well edit these values below. Otherwise, this will all
# come to a firey crash.

# Linode API key, this can be gotten from your profile in the Linode Manager
API_KEY = "1234567890OmgI<3Pwnies."

# Hostname to update.
HOSTNAME = "home.yourdomain.com"

# URL which outputs your current IP. If the resultant HTML contain an IP, 
# we'll use that one. 
CHECK_URL = "http://checkip.dyndns.org"

# Comment this next line out.
exit("Hey, you! You didn't change any settings. How do you expect this script to work?")


#######################################################################
# You should probably stop editing stuff here unless you know what you're doing...

try:
    from linode import api
except:
	exit("Doesn't look like you have the linode-python library installed.")

import re
import urllib2

def get_ip():
    needle = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    ip = None

    try:
        haystack = urllib2.urlopen(CHECK_URL).read()
    except:
        print("Unable to open check URL.")
        exit(-1)

    match = re.search(needle, haystack)
    if match is not None:
        ip = match.group(0)
    else:
        print("Unable to get IP from check URL.")
        exit(-1)

    return ip    

def main():
    # Find our domain record
    domain_id = None
    domain_name = None
    resource_id = None

    linode = api.Api(API_KEY)
    for domain in linode.domain_list():
        if domain['DOMAIN'] in hostname:
            domain_id = domain['DOMAINID']
            domain_name = domain['DOMAIN']
    
    if domain_id is None:
        print("Unable to find the domain in your account. Is your API key correct?")
        return -2

    for resource in linode.domain_resource_list(domainid=domain_id):
        print(resource)

    return 0
    
    ip = get_ip()

    # Is our record already up to date?

    return 0

    # Update the record
    return 1
    

if __name__ == "__main__":
    exit(main())

