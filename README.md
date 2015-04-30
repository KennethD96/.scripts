.scripts
===
This is a collection of scripts and snippets I have made to various tasks.

###ddnsc.py
This is a customizable Dynamic DNS client that support most HTTP-based DDNS services.
It supports authentication by inline-URL and basic HTTP-Auth (Maybe. I don't actually remember if I got it to work ;D)

Configuration:
```
1. Copy the "Config" section of the script to a file named "ddnsc_conf.py" in your working directory (This sucks, I know)
2. Edit the "ddns_update_url" variable with the update URL for either IPv4, IPv6 or both provided by your DDNS-service
3. Add the "<address>" placeholder in the ip-address position of the URL (Or ignore it completely and add your preferred address manually)
4. If your service uses HTTP-auth add your credentials to the "ddns_http_auth" variable for each address-family (Optional)
5. Set the "mode" variable to "dual", "v6" or "v4" to update both or just one address family.
6. Use the "address_scope" variable to set whether to Send your local or globally routable IPv4 address (IPv4 only)
7. Test that everything is working.
```

###mpchc.py
This is a script I made to launch MPC-HC with a time-delay after I have put in a movie disc.
It also supports passing command-line arguments and unicode paths (using Cygwin).
It can also be configured to have a delay, pass certain arguments or open a specific path by default (Unless overridden from the command-line)

Usage: `mpchc [-w <seconds>] [path to media] [MPC-HC Command-line Switches]` (All arguments are optional)

Executable path for both Windows and Cygwin can be configured from the mpchc variable.

###parsev6.py
This is a random snippet I made to try parsing and uncompressing an IPv6 address from a string

 Usage-example:
```
from parsev6 import parsev6
print("Uncompressed IPv6: " + parsev6(raw_input("Please input IPv6-address: "))[0])
```
