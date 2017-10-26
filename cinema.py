#!/usr/bin/python
#encoding: utf-8

lang = {
    "QhueLibMissingMessage": "Missing lib: Qhue. Philips Hue functionality will be disabled.",
    "CouldNotLoadAuraSDKMsg": "Could not load Aura SDK dll: %s",
    "CouldNotLoadConfErrMsg": "Could not open Configuration file"
}

try:
    import qhue
except ImportError:
    print(lang["QhueLibMissingMessage"])

from subprocess import Popen
from sys import argv
from os import path

import json
import ctypes

CONFIGDIR = "config"
CONFIGFILE = "cinema.conf"
LIBDIR = "lib"
AuraSDKdll = "AURA_SDK.dll"

BASEDIR = path.dirname(path.realpath(__file__))
CONFIG = path.join(BASEDIR, CONFIGDIR, CONFIGFILE)
LIBS = path.join(BASEDIR, LIBDIR)

print(CONFIG)
if path.isfile(CONFIG):
    try:
        config = open(CONFIG, "r").read()
        config = json.loads(config)
    except ImportError:
        print(lang["CouldNotLoadConfErrMsg"])

ConfigDefault = {
    "username": None,
    "ip": "",
    "rooms": [1,2],
    "EnableAura": True
}

#try:
#    AuraSDKdllPath = path.join(path.realpath(__file__), libPath, AuraSDKdll)
#    print(AuraSDKdllPath)
#    AuraSDKdll = ctypes.WinDLL(AuraSDKdll)
#except ImportError:
#    print(lang["CouldNotLoadAuraSDKMsg"] % AuraSDKdll)

# Connect to bridge
bridge = qhue.Bridge(config["ip"], config["username"])
args = (argv[1::] if len(argv[1::]) > 0 else [None])

def setLightsState(lights, state):
    for i in lights:
        bridge.groups[i].action(on=state)

def toggleLightsState(lights):
    for i in lights:
        if bridge.groups[i]()["action"]["on"] == True:
            setLightsState([i], False)
        else:
            setLightsState([i], True)

def listLightProperties():
    print(  json.dumps(bridge.lights(),
            sort_keys=True,
            indent=4,
            separators=(',', ': '))
    )

if args[0] == "lights":
    listLightProperties()
elif args[0] == "togglelights":
    toggleLightsState(config["rooms"])
elif args[0] == "lightsoff":
    setLightsState(config["rooms"], False)
elif args[0] == "lightson":
    setLightsState(config["rooms"], True)
else:
    listLightProperties()
