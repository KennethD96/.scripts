#!/usr/bin/python

lang = {
    "QhueLibMissingMessage": "Missing lib: Qhue. Philips Hue functionality will be disabled.",
    "CouldNotLoadAuraSDKMsg": "Could not load Aura SDK dll: %s",
    "CouldNotLoadConfErrMsg": "Could not open Configuration file",
    "HueUsernameCreateTimeOut": "Did not press link button before time-out.",
    "HueErrDisabled": "There was an error enabling Hue. Hue will be disabled."
}

from subprocess import Popen
from sys import argv, exit
from os import path, makedirs
import json

CONFIGDIR = "config"
CONFIGFILE = "cinema.conf"
LIBDIR = "lib"
AURASDKDLL = "AURA_SDK.dll"

BASEDIR = path.dirname(path.realpath(__file__))
CONFIGDIRPATH = path.join(BASEDIR, CONFIGDIR)
CONFIG = path.join(CONFIGDIRPATH, CONFIGFILE)
LIBS = path.join(BASEDIR, LIBDIR)
AURASDK = path.join(LIBS, AURASDKDLL)

args = (argv[1::] if len(argv[1::]) > 0 else [None])

ConfigDefault = {
    "username": None,
    "ip": "",
    "rooms": [1,2],
    "EnableAura": False,
    "EnableHue": True
}

params = {
    "Aura": {
        "shortflag": "a",
        "longflag": "aura",
        "description": "Enable Aura support",
        "state": False,
        "value": False
    },
    "Hue": {
        "shortflags": "h",
        "longflag": "hue",
        "description": "Enable Hue support",
        "state": False,
        "value": False
    }
}

actions = {
    "listlights": {
        "description": "Print information for all available lights.",
        "state": False
    },
    "togglelights": {
        "description": "Toggle the state of all lights.",
        "state": False
    },
    "lightsoff": {
        "description": "Turn off all lights.",
        "state": False
    },
    "lightson": {
        "description": "Turn on all lights.",
        "state": False
    }
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
            if not i in config:
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

if config["EnableAura"]:
    import ctypes
    try:
        aura = ctypes.WinDLL(AURASDK)
    except ImportError:
        print(lang["CouldNotLoadAuraSDKMsg"] % AURASDKDLL)

# Connect to bridge
if config["EnableHue"]:
    try:
        import qhue
        bridge = qhue.Bridge(config["ip"], config["username"])
        test = bridge.lights()
    except ImportError:
        print(lang["QhueLibMissingMessage"])
    except qhue.qhue.QhueException:
        try:
            config["username"] = qhue.create_new_username(config["ip"])
            bridge = qhue.Bridge(config["ip"], config["username"])
            writeConfig(CONFIG, config)
        except qhue.qhue.QhueException:
            print(lang["HueUsernameCreateTimeOut"])
            exit()
    finally:
        config["EnableHue"] = False
        print(lang["HueErrDisabled"])

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
