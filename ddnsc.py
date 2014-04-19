#!/usr/bin/python
#encoding: utf-8
import urllib2
import socket
import sys
########################

'''Fill in the URL used to update DDNS. Add "<address>" if IP-address is included in the URL.'''
#ddns_update_url = "http://dyn.dns.he.net/nic/update?hostname=<userID>&myip=<address>"
ddns_update_url = {
	6: "http://freedns.afraid.org/dynamic/update.php?ABCD1&address=<address>", # IPv6
	4: "http://freedns.afraid.org/dynamic/update.php?ABCD2&address=<address>", # IPv4
}

'''Fill HTTP login if DDNS provider uses HTTP for authentication (HE.net is known to do this) or "None" if not.'''
ddns_http_auth = {
	"login":	"1337",
	"password":	"test123",
	"realm":	"",
}

'''Should I update only IPv6, only IPv4 or both?
Valid options: "v6", "v4", "Both" '''
mode = "both"

'''Should I send your Global or Local address? (IPv4-only)'''
address_scope = "global"

'''This is the URL used to fetch your global IPv4 address'''
get_ip4_url = "http://ip.dnsexit.com/"

'''Send Debug-info to the console.'''
debug = True

########################

if "-6" in sys.argv[1::]:
	mode = "v6"
elif "-4" in sys.argv[1::]:
	mode = "v4"

ddns_addresses = []
ddns_response = ""

def log_str(string):
	print(string)

if mode.lower() == "v6" or mode.lower() == "both":
	s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
	s.connect(('2001:db8::', 0))
	ddns_addresses.append(s.getsockname()[0])
	if debug:
		log_str("Found address: \"%s\"" % s.getsockname()[0])
if mode.lower() == "v4" or mode.lower() == "both":
	if address_scope == "Local":
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('255.255.255.255', 0))
		address = s.getsockname()[0]
	else:
		address = urllib2.urlopen(get_ip4_url).read().strip()
	ddns_addresses.append(address)
	if debug:
		log_str("Found address: \"%s\"" % address)

for address in ddns_addresses:
	ip_ver = 6 if ":" in address else 4
	if "<address>" in ddns_update_url[ip_ver]:
		ddns_update_url_tmp = ddns_update_url[ip_ver].replace("<address>", address)
		try:
			ddns_response = urllib2.urlopen(ddns_update_url_tmp, address)
		except urllib2.HTTPError as err:
			if err == "HTTP Error 401: Authorization Required":
				auth_handler = urllib2.HTTPBasicAuthHandler()
				auth_handler.add_password(
					realm=ddns_http_auth["realm"],
					uri=ddns_update_url_tmp,
					user=ddns_http_auth["login"],
					passwd=ddns_http_auth["password"])
				opener = urllib2.build_opener(auth_handler)
				urllib2.install_opener(opener)
				ddns_response = urllib2.urlopen(ddns_update_url_tmp, address)
		log_str("Attempted update. Got response: \"%s\"" % ddns_response.read().strip("\n"))