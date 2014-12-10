import re

# Takes a string with any IPv6 address and decompress it then
# returns a tuple with the decompressed address as a string,
# as well as a list with every section, a string with the full binary address
# and the binary values for each field.

def parsev6(addr):
	addr = addr.strip("[]").lower()
	if re.findall("[^0-9a-f:]+", addr):
		raise SyntaxError("Address can only contain hex characters")
	else:
		addr = addr.replace("::", ":x:").split(":")
		hex_out, bin_out = [], []
	try:
		addr.remove("")
	except:
		pass

	if addr.count("x") == 1:
		xpos = addr.index("x")
		addr.remove("x")
		while len(addr) < 8:
			addr.insert(xpos, "0000")
	elif addr.count("x") > 1:
		raise SyntaxError("Zero's can only be omitted once")

	for item in addr:
		item_bin = bin(int(item, 16)).replace("0b", "")
		if len(item) > 4:
			raise SyntaxError("Each section cannot contain more than 4 numbers")
		while len(item) < 4:
			item = "0" + item
		while len(item_bin) < 16:
			item_bin = "0" + item_bin
		hex_out.append(item)
		bin_out.append(item_bin)

	if len(addr) < 8:
		raise SyntaxError("Incomplete address")
	elif len(addr) > 8:
		raise SyntaxError("Invalid address")
	output = (
		":".join(hex_out),
		hex_out, "".join(bin_out),
		bin_out
	)
	return output

# Minimalistic version of the function above without any syntax checking.
# Use at your own risk.

def parsev6min(addr):
	addr = addr.lower().strip("[]")
	addr = addr.replace("::", ":x:").split(":")
	hex_out, bin_out = [], []

	try:
		addr.remove("")
	except:
		pass

	if addr.count("x") == 1:
		xpos = addr.index("x")
		addr.remove("x")
		while len(addr) < 8:
			addr.insert(xpos, "0000")

	for item in addr:
		item_bin = bin(int(item, 16)).replace("0b", "")
		while len(item) < 4:
			item = "0" + item
		while len(item_bin) < 16:
			item_bin = "0" + item_bin
		hex_out.append(item)
		bin_out.append(item_bin)
	
	output = (
		":".join(hex_out),
		hex_out, "".join(bin_out),
		bin_out
	)
	return output

#input = "[2001:db8:42::1337]"
#
#print parsev6(input)[0]
#print parsev6min(input)[0]