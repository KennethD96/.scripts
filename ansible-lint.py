#!/usr/bin/python3
# encoding: utf-8
from subprocess import run
import sys
import os

args = [
    "wsl",
    "--shell-type",
    "login",
    "ansible-lint"
]

for arg in sys.argv[1::]:
    print(arg)
    if (os.path.isabs(arg)):
        arg = '$(wslpath -a %r)' % arg
    args.append(arg)

print(args)
run(args)
