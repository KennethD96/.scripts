#!/usr/bin/python
# encoding: utf-8

########################################################################################
# A light-weight python-based DDNS Client supporting v6 and v4 with customizable URL's #
########################################################################################

import urllib2
import base64
import socket
import time
import sys

from os import path
########################

'''Fill in the URL(s) used to update DDNS. Add "<address>" if IP-address is included in the URL.'''
ddns_update_url = {
    6: "http://dyn.dns.he.net/nic/update?hostname=domain6.example.com&myip=<address>",
    4: None,
}

'''Fill in login information if DDNS provider use HTTP for authentication (HE.net is known to do this) or "None" if not.'''
ddns_http_auth = {
    6: ["domain4.example.com", "AnAmazingPassword"],
    4: [None, None]
}

'''Should I update only IPv6, only IPv4 or both?
Valid options: "v6", "v4", "dual" or "auto" if the provider use auto-detect.'''
mode = "dual"

'''Should I send your Global or Local address? (IPv4-only)'''
address_scope = "global"

'''This is the URL used to fetch your global IPv4 address'''
get_ip4_url = "http://ip.dnsexit.com/"

'''Send Debug-info to the console.'''
debug = True

########################

if path.exists("conf.py"):
    from conf import *

log_level = 1 if debug is True else 2
if "-6" in sys.argv[1::]:
    mode = "v6"
elif "-4" in sys.argv[1::]:
    mode = "v4"

ddns_addresses = []
ddns_response = {}
http_response = {}


def log_str(lvl, string):
    level = {
        1: "DEBUG",
        2: "ERROR",
        3: "WARNING",
        4: "INFO",
    }
    pref = "%s %s: " % (
        time.strftime("%d.%m.%Y %H:%M:%S"),
        level[lvl]
    )
    if log_level <= lvl:
        print pref + string

if mode.lower() == "v6" or mode.lower() == "dual":
    try:
        s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        s.connect(('2001:db8::', 0))
        ddns_addresses.append(s.getsockname()[0])
        log_str(1, 'Found address IPv6: \"%s\"' % s.getsockname()[0])
    except socket.error:
        log_str(2, 'Could not fetch IPv6 address.')
if mode.lower() == "v4" or mode.lower() == "dual":
    try:
        if address_scope.lower() == "local":
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('255.255.255.255', 0))
            address = s.getsockname()[0]
        else:
            address = urllib2.urlopen(get_ip4_url).read().strip()
        ddns_addresses.append(address)
        log_str(1, 'Found address IPv4: \"%s\"' % address)
    except socket.error:
        log_str(2, 'Could not fetch local IPv4 address.')
    except urllib2.URLError:
        log_str(2, 'Could not fetch global IPv4 address.')

for address in ddns_addresses:
    ip_ver = 6 if ":" in address else 4
    ddns_update_url_tmp = ddns_update_url[ip_ver]
    if "<address>" in ddns_update_url[ip_ver].lower():
        ddns_update_url_tmp = ddns_update_url_tmp.replace("<address>", address)
    try:

        log_str(1, 'Attempting update with URL: \"%s\"' % ddns_update_url_tmp)
        req = urllib2.Request(ddns_update_url_tmp)
        http_response[ip_ver] = urllib2.urlopen(req).read().strip("\n")
    except urllib2.HTTPError as err:
        log_str(1, 'Got error: "%s"' % err)
        if "HTTP Error 401: Authorization Required" in str(err):
            if not ddns_http_auth[ip_ver][0] == None:
                log_str(1, "Attempting HTTP authentication.")
                base64_auth_string = base64.encodestring("%s:%s" % (
                    ddns_http_auth[ip_ver][0],
                    ddns_http_auth[ip_ver][1])
                )
                req.add_header(
                    "Authorization",
                    "Basic %s" %
                    (base64_auth_string)
                )
                http_response[ip_ver] = urllib2.urlopen(req).read().strip("\n")
            else:
                log_str(3, 'No login information specified. Skipping update.')
    try:
        ddns_response[ip_ver] = http_response[ip_ver]
        log_str(1, "Received response: \"%s\"" % http_response[ip_ver])
    except:
        pass

for ip_ver, item in ddns_response.iteritems():
    log_str(4, '(IPv%s) %s' % (ip_ver, item))
