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
from os import path, makedirs

import json
import ctypes

CONFIGDIR = "config"
CONFIGFILE = "cinema.conf"
LIBDIR = "lib"
AuraSDKdll = "AURA_SDK.dll"

BASEDIR = path.dirname(path.realpath(__file__))
CONFIGDIRPATH = path.join(BASEDIR, CONFIGDIR)
CONFIG = path.join(CONFIGDIRPATH, CONFIGFILE)
LIBS = path.join(BASEDIR, LIBDIR)

ConfigDefault = {
    "username": None,
    "ip": "",
    "rooms": [1,2],
    "EnableAura": False,
    "EnableHue": False
}

def writeConfig(configFile, config):
    f = open(configFile, "w")
    f.write(
            json.dumps(
            config,
            sort_keys=True,
            indent=4,)
    )

def readConfig(configFile):
    try:
        config = open(configFile, "r").read()
        config = json.loads(config)
        configChanged = False
        for i, v in ConfigDefault.items():
            if i in config:
                pass
            else:
                config[i] = v
                configChanged = True
        if configChanged:
            writeConfig(configFile, config)
        return(config)
    except IOError:
        print(lang["CouldNotLoadConfErrMsg"])
        return(ConfigDefault)

if path.isfile(CONFIG):
    config = readConfig(CONFIG)
else:
    if not path.exists(CONFIGDIRPATH):
        makedirs(CONFIGDIRPATH)
    config = ConfigDefault
    writeConfig(config)


#try:
#    AuraSDKdllPath = path.join(path.realpath(__file__), libPath, AuraSDKdll)
#    print(AuraSDKdllPath)
#    AuraSDKdll = ctypes.WinDLL(AuraSDKdll)
#except ImportError:
#    print(lang["CouldNotLoadAuraSDKMsg"] % AuraSDKdll)

# Connect to bridge
if config["EnableHue"]:
    bridge = qhue.Bridge(config["ip"], config["username"])
args = (argv[1::] if len(argv[1::]) > 0 else [None])

def setHueLightsState(lights, state):
    if config["EnableHue"]:
        for i in lights:
            bridge.groups[i].action(on=state)

def toggleHueLightsState(lights):
    if config["EnableHue"]:
        for i in lights:
            if bridge.groups[i]()["action"]["on"] == True:
                setHueLightsState([i], False)
            else:
                setHueLightsState([i], True)

def listHueLightProperties():
    if config["EnableHue"]:
        print(  json.dumps(bridge.lights(),
                sort_keys=True,
                indent=4,
                separators=(',', ': '))
        )

if args[0] == "lights":
    listHueLightProperties()
elif args[0] == "togglelights":
    toggleHueLightsState(config["rooms"])
elif args[0] == "lightsoff":
    setHueLightsState(config["rooms"], False)
elif args[0] == "lightson":
    setHueLightsState(config["rooms"], True)
else:
    listHueLightProperties()
