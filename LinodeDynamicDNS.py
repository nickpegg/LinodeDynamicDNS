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
	import linode-python
except:
	exit("Doesn't look like you have the linode-python library installed.")

import re
import urllib2


