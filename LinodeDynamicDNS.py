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
    # This is only needed because we want to be nice and not hammer Linode
    # If we weren't nice, we could just set TARGET='[remote_addr]' 
    # in the DNS resource update.
    
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
    resource_id = None
    domain_name = None  # Example: example.com
    host_name = None    # Example: home (from home.example.com)
    
    ip = get_ip()

    # Login and test the connection
    try:
        linode = api.Api(API_KEY)
        linode.test_echo()
    except:
        print("Unable to login to the Linode API. Is your API key correct?")
        return -2

    # Find the domain name and ID
    for domain in linode.domain_list():
        if domain['DOMAIN'] in HOSTNAME:
            domain_id = domain['DOMAINID']
            domain_name = domain['DOMAIN']
            host_name = HOSTNAME.replace("." + domain_name, '')
    
    if domain_id is None:
        print("Unable to find the domain in your account.")
        return -2

        
    # Find the domain resource and ID
    for resource in linode.domain_resource_list(domainid=domain_id):
        if resource['NAME'] == host_name:
            resource_id = resource['RESOURCEID']
            resource_ip = resource['TARGET']
    
    if resource_id is None: 
        # We need to create the hostname
        try:
            resource_id = linode.domain_resource_create(domainid=domain_id, 
                name=host_name, type='A', target="[remote_addr]")['ResourceID']
        except:
            print("%s doesn't exist and I was unable to create it." % HOSTNAME)
            return -2
        
        print("Successfully created %s with the IP %s" % (HOSTNAME, ip))
        return 1
        

    # Update the record if it's wrong
    if resource_ip != ip:
        try:
            linode.domain_resource_update(domainid=domain_id, 
                resourceid=resource_id, name=host_name, target=ip)
        except:
            print("%s exists but I was unable to update it." % HOSTNAME)
            return -2

        print("Successfully updated %s with the IP %s" % (HOSTNAME, ip))
        return 1
    else:   
        return 0    # Quit silently, useful for cron jobs
        
    

if __name__ == "__main__":
    exit(main())