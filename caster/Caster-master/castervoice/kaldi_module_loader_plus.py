"""
Command-module loader for Kaldi.

This script is based on 'dfly-loader-wsr.py' written by Christo Butcher and
has been adapted to work with the Kaldi engine instead.

This script can be used to look for Dragonfly command-modules for use with
the Kaldi engine. It scans the directory it's in and loads any ``_*.py`` it
finds.
"""


# TODO Have a simple GUI for pausing, resuming, cancelling and stopping
# recognition, etc

from __future__ import print_function

import logging
import os.path
import sys
import threading
import six

from dragonfly import BringApp, WaitWindow, Key, FocusWindow, Mimic, PlaySound, Mouse, Choice
from configparser import ConfigParser
from dragonfly import get_engine
from dragonfly import Grammar, MappingRule, Function, Dictation, FuncContext
from dragonfly.loader import CommandModuleDirectory
from dragonfly.log import setup_log


# --------------------------------------------------------------------------
# Set up basic logging.
def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

if False:
    # Debugging logging for reporting trouble
    logging.basicConfig(level=10)
    logging.getLogger('grammar.decode').setLevel(20)
    logging.getLogger('grammar.begin').setLevel(20)
    logging.getLogger('compound').setLevel(20)
    logging.getLogger('kaldi.compiler').setLevel(10)
else:
    setup_log()

def noop():
    #noop
    pass

def readIni(propName):
    iniURL = r"C:\Users\loves\programming\humanInterface\ahk\inis\globals.ini"
    confparser = ConfigParser()
    confparser.read(iniURL)
    return confparser.get('globals', propName)

def writeIni(propName,propValue):
    iniURL = r"C:\Users\loves\programming\humanInterface\ahk\inis\globals.ini"
    confparser = ConfigParser()
    confparser.read(iniURL)
    confparser['globals'][propName] = propValue
    with open(iniURL, 'w') as configfile:
        confparser.write(configfile)

def setFootPedalMode(footPedalMode="click"):
    writeIni("footMode",footPedalMode)

def setControllerMode(onOff="on"):
    writeIni("controllerMode",onOff)

def load_custom_keys():
    foot_pedal_modes = {
        "scroll":"scroll",
        "click":"click"
    }
    grammar = Grammar("customKeys")
    class CustomKeysRule(MappingRule):
        mapping = {
            "windows": Key('win:down/3, win:up/3'),
            "caster reboot": Mimic("reboot caster"),
            "magic":Mouse("left:down/3, left:up/3"),
            "space bar":Key("space:down/3, space:up/3"),
            "foot pedal <footPedalMode>":Function(setFootPedalMode),
            "ecks box controller <onOff>":Function(setControllerMode),
            "look":Key("f15")
            # "foot pedal mouse":Function(lambda:writeIni("footMode","mouse"))
        }
        extras = [
            Choice("footPedalMode",foot_pedal_modes),
            Choice("onOff",{"on":"on","off":"off"})
        ]
    grammar.add_rule(CustomKeysRule())
    grammar.load()

def closeProgram(name):
    (FocusWindow(title=name) + WaitWindow(title=name) + Key('a-f4')).execute()

def load_eye_control():
    eye_grammar = Grammar("eyeControl")

    def startTrackingPrograms():
        BringApp(r'C:\Users\loves\programming\humanInterface\openeViacam.bat').execute()
        BringApp(r'C:\Users\loves\programming\humanInterface\openPrecisionGazeMouse.bat').execute()

    def stopTrackingPrograms():
        closeProgram("Precision Gaze Mouse")
        closeProgram("Enable Viacam")
    class EyeControlRule(MappingRule):
        mapping = {
            "caster please toggle eye tracking": Key('f10') + Key('f11'),
            # "caster please enable eye control": Key('f10'),
            # "caster please disable eye control":   Function(stopTrackingPrograms)
        }
    eye_grammar.add_rule(EyeControlRule())
    eye_grammar.load()


# --------------------------------------------------------------------------
# User notification / rudimentary UI. MODIFY AS DESIRED

# For message in ('sleep', 'wake')
def notify(message):
    if message == 'sleep':
        PlaySound(r"C:\Windows\Media\Speech Off.wav").execute()

        print("Sleeping...")
        # get_engine().speak("Sleeping")
    elif message == 'wake':
        print("Awake...")
        PlaySound(r"C:\Windows\Media\Speech On.wav").execute()

        # get_engine().speak("Awake")


# --------------------------------------------------------------------------
# Sleep/wake grammar. (This can be unused or removed if you don't want it.)

sleeping = False

def load_sleep_wake_grammar(initial_awake):
    sleep_grammar = Grammar("sleep")
    def sleep(force=False):
        get_engine().stop_saving_adaptation_state()
        global sleeping
        if not sleeping or force:
            sleeping = True
            sleep_grammar.set_exclusiveness(True)
            notify('sleep')

    def wake(force=False):
        get_engine().start_saving_adaptation_state()
        global sleeping
        if sleeping or force:
            sleeping = False
            sleep_grammar.set_exclusiveness(False)
            notify('wake')

    class SleepRule(MappingRule):
        mapping = {
            "go to sleep":Function(sleep),
            "bake up": Function(noop),
            "rake up":Function(noop),
            "shake up":Function(noop),
            "lake up":Function(noop),
            "nake up":Function(noop),
            "wake tup":Function(noop),
            "wake sup":Function(noop),
            "whey grub":Function(noop),
            "wake":Function(noop),
            "wake up":Function(wake),
        }
    sleep_grammar.add_rule(SleepRule())

    sleep_noise_rule = MappingRule(
        name = "sleep_noise_rule",
        mapping = { "<text>": Function(lambda text: False and print("(asleep) " + text)) },
        extras = [ Dictation("text") ],
        context = FuncContext(lambda: sleeping),
    )
    sleep_grammar.add_rule(sleep_noise_rule)

    sleep_grammar.load()

    # def checkIniFile():
    #     global sleeping
    #     global sleepOverride
    #     voice = readIni('voice')
    #     new_value = (voice=="off")
    #     if new_value:
    #         sleep()
    #     else:
    #         wake()
            
    # set_interval(checkIniFile,3)
    # watchingIniFile = True
        
    



    if initial_awake:
        wake(force=True)
    else:
        sleep(force=True)


# --------------------------------------------------------------------------
# Main event driving loop.
def load_custom_grammars():
    load_eye_control()
    load_sleep_wake_grammar(True)
    load_custom_keys()



def main():
    logging.basicConfig(level=logging.INFO)

    try:
        path = os.path.dirname(__file__)
    except NameError:
        # The "__file__" name is not always available, for example
        # when this module is run from PythonWin.  In this case we
        # simply use the current working directory.
        path = os.getcwd()
        __file__ = os.path.join(path, "kaldi_module_loader_plus.py")

    # Set any configuration options here as keyword arguments.
    # See Kaldi engine documentation for all available options and more info.
    engine = get_engine('kaldi',
        # model_dir='kaldi_model',  # default model directory
        # vad_aggressiveness=3,  # default aggressiveness of VAD
        # vad_padding_start_ms=150,  # default ms of required silence before VAD
        # vad_padding_end_ms=150,  # default ms of required silence after VAD
        # vad_complex_padding_end_ms=500,  # default ms of required silence after VAD for complex utterances
        # input_device_index=None,  # set to an int to choose a non-default microphone
        # lazy_compilation=True,  # set to True to parallelize & speed up loading
        # retain_dir=None,  # set to a writable directory path to retain recognition metadata and/or audio data
        # retain_audio=None,  # set to True to retain speech data wave files in the retain_dir (if set)
    )

    # Call connect() now that the engine configuration is set.
    engine.connect()

    # Load grammars.
    load_sleep_wake_grammar(True)
    directory = CommandModuleDirectory(path, excludes=[__file__])
    directory.load()

    # Define recognition callback functions.
    def on_begin():
        print("Speech start detected.")

    def on_recognition(words):
        message = u"Recognized: %s" % u" ".join(words)

        # This only seems to be an issue with Python 2.7 on Windows.
        if six.PY2:
            encoding = sys.stdout.encoding or "ascii"
            message = message.encode(encoding, errors='replace')
        print(message)

    def on_failure():
        print("Sorry, what was that?")

    # Start the engine's main recognition loop
    engine.prepare_for_recognition()
    try:
        print("Listening...")
        engine.do_recognition(on_begin, on_recognition, on_failure)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
