# LinodeDynamicDNS.py

Just a little script to dynamically update a DNS record in Linode's DNS
service. Requires [linode-python](https://github.com/tjfontaine/linode-python/)
and Python 2.x (since linode-python is not Python 3 compatible).

This script is best ran as a cronjob. It only outputs anything on an error, if
it had to create a record, or if it updated a record.

Don't forget to change the settings at the top of the script before 
trying to use it!
