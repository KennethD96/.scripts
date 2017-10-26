#!/usr/bin/python
# encoding: utf-8
from subprocess import Popen
from time import sleep
import platform
import sys
import os

##########################################################################################
# Usage: mpchc [-t <seconds>] [path to media] [MPC-HC Command-Line Switches]
# This is a interface to launch MPC-HC with a optional delay and also includes a set of
# Variables to set default options to use when MPC-HC is launched.
# Warning: For paths containing unicode characters use cygwin!
#
# Personally I use the script with AnyDVD HD to launch MPC-HC when a disc is inserted
# It requires a 5 second delay to wait while the disc is mounting.
##########################################################################################

mpchc_path = {
    "windows": "C:\Program Files (x86)\MPC-HC\mpc-hc.exe",
    "cygwin": "/cygdrive/c/Program Files (x86)/MPC-HC/mpc-hc.exe"
}

mpc_args = []       # Contains a list of default switches to pass to MPC-HC.
open_path = ""      # Default path to use unless path is specified.
launch_delay = 0    # The default delay to wait before launching the player.

##########################################################################################

mpchc_exe = mpchc_path["windows"] if platform.system() == "Windows" else mpchc_path["cygwin"]
args = sys.argv[1::]

# Parse options for the script.
usage_str = "Usage: mpchc [-t <seconds>] [path to media] [MPC-HC Command-Line Switches]"
if len(args) > 0:
    if args[0].startswith("-") and len(args[0]) == 2:
        if args[0] == "-t" and len(args) > 1:
            if args[1].isdigit():
                launch_delay = int(args[1])
                args.pop(1)
            else:
                print(usage_str)
        else:
            print(usage_str)
        args.pop(0)

# If first arg is number, exterminate!
if len(args) > 0:
    if args[0].isdigit():
        args.pop(0)

# Remove quotation marks left over from bad terminals.
if "\"" in "".join(args):
    args = " ".join(args).split("\"")

# Find Video path (if any).
if len(args) > 0:
    if (
            args[0].count("/") > 1
            or "." in args[0]
            or ":" in args[0]
    ):

        args[0] = args[0].strip("\"")
        if os.path.isabs(args[0]):
            if args[0].endswith("\\"):
                args[0] = args[0][:-1]
            open_path = args[0]
            args.pop(0)
        elif ":" in args[0]:
            open_path = args[0]
            args.pop(0)
        else:
            open_path = os.path.join(os.getcwd(), args[0])
            args.pop(0)

        if "cygwin" in platform.system().lower():
            if open_path.startswith("/cygdrive/"):
                open_path = open_path.replace("/cygdrive/", "", 1)
                open_path = open_path.split("/")
                open_path[0] = open_path[0] + ":"
                open_path = "/".join(open_path)

# Patch everything together.
if len(args) > 0:
    for arg in args:
        mpc_args.append(arg)
if len(open_path) > 0:
    mpc_args.insert(0, open_path)
mpc_args.insert(0, mpchc_exe)

# Launch MPC-HC/Player.
if os.path.exists(mpchc_exe):
    if launch_delay > 0:
        sleep(launch_delay)
    Popen(mpc_args)
else:
    print("MPC-HC Is not installed in the specified path.")
