# LinodeDynamicDNS.py

Just a little script to dynamically update a DNS record in Linode's DNS
service. Requires [linode-python](http://atxconsulting.com/projects/linode-api)
and (for the moment) Python 2.x. 

This script best ran as a cronjob. It only outputs anything on an error, if
it had to create a record, or if it updated a record.

Don't forget to change the settings at the top of the script before 
trying to use it!
