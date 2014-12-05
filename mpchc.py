#encoding: utf-8
from subprocess import Popen
from time import sleep
import sys, os, platform

args = sys.argv[1::]
if platform.system() == "Windows":
    mpchc_exe = "C:\Program Files (x86)\MPC-HC\mpc-hc.exe"
else:
    mpchc_exe = "/cygdrive/c/Program Files (x86)/MPC-HC/mpc-hc.exe"

mpc_args = []
open_path = ""
delay = 0

usage_str = "Usage: mpchc.py [-w <seconds>] [Path to file] [MPC-HC Options]"
if len(args) > 0:
    if  args[0].startswith("-") and len(args[0]) == 2:
        if args[0] == "-w" and len(args) > 1:
            if args[1].isdigit():
                delay = int(args[1])
                args.pop(1)
            else:
                print(usage_str)
        else:
            print(usage_str)
        args.pop(0)

if len(args) > 0:
    if args[0].isdigit():
        args.pop(0)

if "\"" in "".join(args):
    args = " ".join(args).split("\"")

if len(args) > 0:
    if "." in args[0] or ":" in args[0]:
        if not "cygwin" in platform.system().lower():
            args[0] = args[0].strip("\"")
            if not os.path.isabs(args[0]):
                open_path = os.path.join(os.getcwd(), args[0])
                args.pop(0)
            else:
                if args[0].endswith("\\"):
                    args[0] = args[0][:-1]
                open_path = args[0]
                args.pop(0)
        else:
            open_path = args[0]
            args.pop(0)
            if open_path.startswith("/cygdrive/"):
                open_path = open_path.replace("/cygdrive/", "", 1)
                open_path = open_path.split("/")
                open_path[0] = open_path[0] + ":"
                open_path = "/".join(open_path)

if len(args) > 0:
    for arg in args:
        mpc_args.append(arg)
if len(open_path) > 0:
    mpc_args.insert(0, open_path)
mpc_args.insert(0, mpchc_exe)

if os.path.exists(mpchc_exe):
    if delay > 0:
        sleep(delay)
    Popen(mpc_args)
else:
    print("MPC-HC Is not installed in specified path.")
