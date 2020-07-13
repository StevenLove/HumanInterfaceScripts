"""A command module for Dragonfly, for generic editing help.

-----------------------------------------------------------------------------
This is a heavily modified version of the _multiedit-en.py script at:
http://dragonfly-modules.googlecode.com/svn/trunk/command-modules/documentation/mod-_multiedit.html  # @IgnorePep8
Licensed under the LGPL, see http://www.gnu.org/licenses/

"""
from time import sleep
from dragonfly import (
    Alternative, AppContext,
    BringApp,
    Choice, CompoundRule, Config, Dictation,
    FocusWindow, Function, Grammar,
    Integer, IntegerRef, Item, Key,
    MappingRule, Mimic, Mouse,
    Pause, Repetition, RuleRef,
    Section, Text, Window,
    get_engine
)
import lib.mappings

import win32con

from dragonfly.actions.keyboard import Typeable, keyboard
from dragonfly.actions.typeables import typeables

if not 'Control_R' in typeables:
    keycode = win32con.VK_RCONTROL
    typeables["Control_R"] = Typeable(code=keycode, name="Control_R")
if not 'semicolon' in typeables:
    typeables["semicolon"] = keyboard.get_typeable(char=';')

import lib.config
config = lib.config.get_config()

import lib.sound as sound
from lib.format import (
    camel_case_count,
    pascal_case_count,
    snake_case_count,
    squash_count,
    expand_count,
    uppercase_count,
    lowercase_count,
    format_text,
    FormatTypes as ft,
)

import json
import os
from win32com.client import Dispatch
from win32com.client.gencache import EnsureDispatch

release = Key("shift:up, ctrl:up, alt:up, win:up")


################################################################################
## Disabling dictation mode
## actually this is handled in kaldi_module_loader_plus.py
## but maybe we can do something similar for setting up modes
dictation_enabled = True

def noop(text=None):
    print "noop"
    pass

# def dictation_off():
#     global dictation_enabled
#     if dictation_enabled:
#         print "Dictation now OFF."
#         dictation_enabled = False
#         grammar.disable()
#         # dictationOffGrammar.enable()
#         # disableDictation()
#     else:
#         print "Dictation already off." 
# def dictation_on():
#     global dictation_enabled
#     if not dictation_enabled:
#         print "Dictation now ON."
#         dictation_enabled = True
#         grammar.enable()
#         # dictationOffGrammar.disable()
#         # enableDictation()
#     else:
#         print "Dictation already on."

# class DictationOffRule(MappingRule):
#     mapping = {
#         # "dictation off | go to sleep": Function(dictation_off),
#         # "dictation on | wake up": Function(dictation_on),
#         "<text>": Function(noop),
#     }
#     extras = [
#         Dictation("text"),
#     ]
#     defaults = {
#     }

# dictationOffGrammar = Grammar("Dictation off")
# dictationOffGrammar.add_rule(DictationOffRule())
# dictationOffGrammar.load()
# dictationOffGrammar.disable()



################################################################################

def cancel_and_sleep(text=None, text2=None):
    """random mumbling go to sleep'" => Microphone sleep."""
    # print("* Dictation canceled. Going to sleep. *")
    sound.play(sound.SND_DING)
    dictation_off()

def copy_command():
    # Add Command Prompt, putty, ...?
    context = AppContext(executable="console")
    window = Window.get_foreground()
    if context.matches(window.executable, window.title, window.handle):
        return
    release.execute()
    Key("c-c/3").execute()

def paste_command():
    # Add Command Prompt, putty, ...?
    context = AppContext(executable="console")
    window = Window.get_foreground()
    if context.matches(window.executable, window.title, window.handle):
        return
    release.execute()
    Key("c-v/3").execute()

################################################################################

formatMap = {
    "camel": ft.camelCase,
    "pascal": ft.pascalCase,
    "studly": ft.pascalCase,
    "snake": ft.snakeCase,
    "uppercase": ft.upperCase,
    "lowercase": ft.lowerCase,
    "squash": ft.squash,
    "lowercase squash": [ft.squash, ft.lowerCase],
    "uppercase squash": [ft.squash, ft.upperCase],
    "squash lowercase": [ft.squash, ft.lowerCase],
    "squash uppercase": [ft.squash, ft.upperCase],
    "dashify": ft.dashify,
    "lowercase dashify": [ft.dashify, ft.lowerCase],
    "uppercase dashify": [ft.dashify, ft.upperCase],
    "dashify lowercase": [ft.dashify, ft.lowerCase],
    "dashify uppercase": [ft.dashify, ft.upperCase],
    "dotify": ft.dotify,
    "lowercase dotify": [ft.dotify, ft.lowerCase],
    "uppercase dotify": [ft.dotify, ft.upperCase],
    "dotify lowercase": [ft.dotify, ft.lowerCase],
    "dotify uppercase": [ft.dotify, ft.upperCase],
    "say": ft.spokenForm,
    "environment variable": [ft.snakeCase, ft.upperCase],
}

abbreviationMap = {
    "administrator": "admin",
    "administrators": "admins",
    "application": "app",
    "applications": "apps",
    "argument": "arg",
    "arguments": "args",
    "attribute": "attr",
    "attributes": "attrs",
    "(authenticate|authentication)": "auth",
    "binary": "bin",
    "button": "btn",
    "class": "cls",
    "command": "cmd",
    "(config|configuration)": "cfg",
    "context": "ctx",
    "control": "ctrl",
    "database": "db",
    "(define|definition)": "def",
    "description": "desc",
    "(develop|development)": "dev",
    "(dictionary|dictation)": "dict",
    "(direction|directory)": "dir",
    "dynamic": "dyn",
    "example": "ex",
    "execute": "exec",
    "exception": "exc",
    "expression": "exp",
    "(extension|extend)": "ext",
    "function": "func",
    "framework": "fw",
    "(initialize|initializer)": "init",
    "instance": "inst",
    "integer": "int",
    "iterate": "iter",
    "java archive": "jar",
    "javascript": "js",
    "keyword": "kw",
    "keyword arguments": "kwargs",
    "language": "lng",
    "library": "lib",
    "length": "len",
    "number": "num",
    "object": "obj",
    "okay": "ok",
    "package": "pkg",
    "parameter": "param",
    "parameters": "params",
    "pixel": "px",
    "position": "pos",
    "point": "pt",
    "previous": "prev",
    "property": "prop",
    "python": "py",
    "query string": "qs",
    "reference": "ref",
    "references": "refs",
    "(represent|representation)": "repr",
    "regular (expression|expressions)": "regex",
    "request": "req",
    "revision": "rev",
    "ruby": "rb",
    "session aidee": "sid",  # "session id" didn't work for some reason.
    "source": "src",
    "(special|specify|specific|specification)": "spec",
    "standard": "std",
    "standard in": "stdin",
    "standard out": "stdout",
    "string": "str",
    "(synchronize|synchronous)": "sync",
    "system": "sys",
    "utility": "util",
    "utilities": "utils",
    "temporary": "tmp",
    "text": "txt",
    "value": "val",
    "window": "win",
}

# For use with "say"-command. Words that are commands in the generic edit
# grammar were treated as separate commands and could not be written with the
# "say"-command. This overrides that behavior.
# Other words that won't work for one reason or another, can also be added to
# this list.
reservedWord = {
    "up": "up",
    "down": "down",
    "left": "left",
    "right": "right",
    "home": "home",
    "end": "end",
    "space": "space",
    "tab": "tab",
    "backspace": "backspace",
    "delete": "delete",
    "enter": "enter",
    "paste": "paste",
    "copy": "copy",
    "cut": "cut",
    "undo": "undo",
    "release": "release",
    "page up": "page up",
    "page down": "page down",
    "say": "say",
    "select": "select",
    "select all": "select all",
    "abbreviate": "abbreviate",
    "uppercase": "uppercase",
    "lowercase": "lowercase",
    "expand": "expand",
    "squash": "squash",
    "dash": "dash",
    "underscore": "underscore",
    "dot": "dot",
    "period": "period",
    "minus": "minus",
    "semi-colon": "semi-colon",
    "hyphen": "hyphen",
    "triple": "triple"
}

################################################################################

grammarCfg = Config("multi edit")
grammarCfg.cmd = Section("Language section")
grammarCfg.cmd.map = Item(
    {
        # Navigation keys.
        "up [<n>]": Key("up:%(n)d"),
        "up [<n>] slow": Key("up/15:%(n)d"),
        "down [<n>]": Key("down:%(n)d"),
        "down [<n>] slow": Key("down/15:%(n)d"),
        "left [<n>]": Key("left:%(n)d"),
        "left [<n>] slow": Key("left/15:%(n)d"),
        "right [<n>]": Key("right:%(n)d"),
        "right [<n>] slow": Key("right/15:%(n)d"),
        "page up [<n>]": Key("pgup:%(n)d"),
        "page down [<n>]": Key("pgdown:%(n)d"),
        "up <n> (page|pages)": Key("pgup:%(n)d"),
        "down <n> (page|pages)": Key("pgdown:%(n)d"),
        "left <n> (word|words)": Key("c-left/3:%(n)d/10"),
        "right <n> (word|words)": Key("c-right/3:%(n)d/10"),
        "home|homer": Key("home"),
        "end": Key("end"),
        "doc home": Key("c-home/3"),
        "doc end": Key("c-end/3"),
        "doc save": Key("c-s"),
        "doc open": Key("c-o"),
        "doc save as": Key("alt:down/3,f/3,a/3,alt:up/3"),
        "doc close [<n>]": Key("c-w:%(n)d"),
        "doc close all": Key("cs-w:%(n)d"),
        "doc next [<n>]": Key("c-tab:%(n)d"),
        "doc create": Key("c-n"),
        "doc new tab": Key("c-t"),
        "doc (previous|back) [<n>]": Key("cs-tab:%(n)d"),
        "doc (search|find)": Key("c-f"),
        "doc print": Key("c-p"),
        "doc format": Key("a-e, v, a"),
        "doc this year": Key("a-d/5, end/5") + Text("&tbs=cdr%%3A1%%2Ccd_min%%3A1+Jan+2019%%2Ccd_max%%3A&tbm=", pause=0.001) + Key("enter"),
        "zoom in": Key("c-plus, c-plus"),
        "zoom out": Key("c-minus, c-minus"),
        "zoom reset": Key("c-0"),
        "select line [<n>]": release + Key("home, home, s-down:%(n)d"),
        "go block start [<n>]": Key("sa-[:%(n)d"),
        "show parameters": Key("cs-space"),
        "integer": Text("int"),
        "variable": Text("var"),
        "uno [<n>]": Key("f1:%(n)d"),
        "doss [<n>]": Key("f2:%(n)d"),
        "trez [<n>]": Key("f3:%(n)d"),
        "quatro [<n>]": Key("f4:%(n)d"),
        "sinko [<n>]": Key("f5:%(n)d"),
        "see ettay [<n>]": Key("f7:%(n)d"),
        "occo [<n>]": Key("f8:%(n)d"),
        "noo evvay [<n>]": Key("f9:%(n)d"),
        "dee ez [<n>]": Key("f10:%(n)d"),
        "onsay [<n>]": Key("f11:%(n)d"),
        "dossay [<n>]": Key("f12:%(n)d"),
        # Functional keys.
        "space": release + Key("space"),
        "space [<n>]": release + Key("space:%(n)d"),
        "(slap|go) [<n>]": release + Key("enter:%(n)d"),
        "tab [<n>]": Key("tab:%(n)d"),
        "delete [<n>]": Key("del/3:%(n)d"),
        "delete [this] line": Key("home, home, s-end, del, del"),  # @IgnorePep8
        "backspace [<n>]": release + Key("backspace:%(n)d"),
        "application key": release + Key("apps/3"),
        "win key": release + Key("win/3"),
        "paste [that]": Function(paste_command),
        "copy [that]": Function(copy_command),
        "cut [that]": release + Key("c-x/3"),
        "select all": release + Key("c-a/3"),
        "undo": release + Key("c-z/3"),
        "undo <n> [times]": release + Key("c-z/3:%(n)d"),
        "redo": release + Key("c-y/3"),
        "redo <n> [times]": release + Key("c-y/3:%(n)d"),
        "[(hold|press)] (alt|meta)": Key("alt:down/3"),
        "release (alt|meta)": Key("alt:up"),
        "[(hold|press)] shift": Key("shift:down/3"),
        "release shift": Key("shift:up"),
        "[(hold|press)] control": Key("ctrl:down/3"),
        "release control": Key("ctrl:up"),
        "(hold|press) (hyper|windows)": Key("win:down/3"),
        "release (hyper|windows)": Key("win:up"),
        "[press] (hyper|windows) first": Key("win:down/3, 1/3, win:up/3"),
        "[press] (hyper|windows) <m>": Key("win:down/3, %(m)d/3, win:up/3"),
        "release [all]": release,
        "git commit minus M": Text("git commit -m "),
        # Closures.
        "angle brackets": Key("langle, rangle, left/3"),
        "brackets": Key("lbracket, rbracket, left/3"),
        "braces": Key("lbrace, rbrace, left/3"),
        "parens": Key("lparen, rparen, left/3"),
        "quotes": Key("dquote/3, dquote/3, left/3"),
        "single quotes": Key("squote, squote, left/3"),
        # To release keyboard capture by VirtualBox.
        "press right control": Key("Control_R"),
        # Formatting <n> words to the left of the cursor.
        "camel case <n> [words]": Function(camel_case_count),
        "pascal case <n> [words]": Function(pascal_case_count),
        "snake case <n> [words]": Function(snake_case_count),
        "squash <n> [words]": Function(squash_count),
        "expand <n> [words]": Function(expand_count),
        "uppercase <n> [words]": Function(uppercase_count),
        "lowercase <n> [words]": Function(lowercase_count),
        # Format dictated words. See the formatMap for all available types.
        # Ex: "camel case my new variable" -> "myNewVariable"
        # Ex: "snake case my new variable" -> "my_new_variable"
        # Ex: "uppercase squash my new hyphen variable" -> "MYNEW-VARIABLE"
        "<formatType> <text>": Function(format_text),
        # For writing words that would otherwise be characters or commands.
        # Ex: "period", tab", "left", "right", "home".
        "Simon says <reservedWord>": Text("%(reservedWord)s"),
        # Abbreviate words commonly used in programming.
        # Ex: arguments -> args, parameterers -> params.
        "abbreviate <abbreviation>": Text("%(abbreviation)s"),
        # Text corrections.
        "(add|fix) missing space": Key("c-left/3, space, c-right/3"),
        "(delete|remove) (double|extra) (space|whitespace)": Key("c-left/3, backspace, c-right/3"),  # @IgnorePep8
        "(delete|remove) (double|extra) (type|char|character)": Key("c-left/3, del, c-right/3"),  # @IgnorePep8
        # Microphone sleep/cancel started dictation.
        "[<text>] (go to sleep|cancel and sleep) [<text2>]": Function(cancel_and_sleep),  # @IgnorePep8

        # Ego
        "alpha": Text("a"),
        "bravo": Text("b"),
        "charlie": Text("c"),
        "delta": Text("d"),
        "echo": Text("e"),
        "foxtrot": Text("f"),
        "golf": Text("g"),
        "hotel": Text("h"),
        "(india|indigo)": Text("i"),
        "juliet": Text("j"),
        "kilo": Text("k"),
        "lima": Text("l"),
        "mike": Text("m"),
        "november": Text("n"),
        "oscar": Text("o"),
        "(Papa|pappa|pepper|popper)": Text("p"),
        "quebec": Text("q"),
        "romeo": Text("r"),
        "sierra": Text("s"),
        "tango": Text("t"),
        "uniform": Text("u"),
        "victor": Text("v"),
        "whiskey": Text("w"),
        "x-ray": Text("x"),
        "yankee": Text("y"),
        "zulu": Text("z"),
        "big alpha": Text("A"),
        "big bravo": Text("B"),
        "big charlie": Text("C"),
        "big delta": Text("D"),
        "big echo": Text("E"),
        "big foxtrot": Text("F"),
        "big golf": Text("G"),
        "big hotel": Text("H"),
        "big india": Text("I"),
        "big juliet": Text("J"),
        "big kilo": Text("K"),
        "big lima": Text("L"),
        "big mike": Text("M"),
        "big november": Text("N"),
        "big oscar": Text("O"),
        "big (Papa|pappa|pepper|popper)": Text("P"),
        "big quebec": Text("Q"),
        "big romeo": Text("R"),
        "big sierra": Text("S"),
        "big tango": Text("T"),
        "big uniform": Text("U"),
        "big victor": Text("V"),
        "big whiskey": Text("W"),
        "big x-ray": Text("X"),
        "big yankee": Text("Y"),
        "big zulu": Text("Z"),
        # Ego
        "quote [<n>]": release + Key("dquote:%(n)d"),
        "dot": Text("."),
        "backslish": Text("\\"),
        "slish": Text("/"),
        "lape": Text("("),
        "rape": Text(")"),
        "lace": Text("{"),
        "race": Text("}"),
        "(lack|bra)": Text("["),
        "(rack|ket)": Text("]"),
        "lang": Text("<"),
        "rang": Text(">"),
        "pipe": Text("|"),
        "eke": Text("="),
        "bang": Text("!"),
        "plus": Text("+"),
        "minus": Text("-"),
        "mull": Text("*"),
        "(underscore|bar) [<n>]": Key("underscore/2:%(n)d"),
        "(sem|semi|rock|semicolon)": Text(";"),
        "(coal|colon)": Text(":"),
        "(comma|cam) [<n>]": Key("comma/2:%(n)d"),
        "(dot|period) [<n>]": Key("dot/2:%(n)d"),
        "(dash|hyphen) [<n>]": Key("hyphen/2:%(n)d"),
        "hash [<n>]": Key("hash/2:%(n)d"),
        #"": Text(""),
        # Ego
        "quit [<n>]": release + Key("escape:%(n)d"),
        "switch [<n>]": release + Key("alt:down/10, tab:%(n)d/10, alt:up"),
        "hut": release + Key("alt:down/5, d, alt:up"),
        "context menu": release + Key("apps"),
        # Ego
        "hash include stud Io": Text("#include <stdio.h>"),
        "hash include stud lib": Text("#include <stdlib.h>"),
        "change directory": Text("cd "),
        "change directory drive": Text("cd /D "),
        "directory list": Text("dir "),
        "strike [<n>]": release + Key("backspace:%(n)d"),
        "kill [<n>]": release + Key("delete:%(n)d"),
        "pig [<n>]": release + Key("pgdown:%(n)d"),
        "pug [<n>]": release + Key("pgup:%(n)d"),
        "comment": Text("// "),
        # Ego
        # "dictation on": Function(dictation_on),
        # "dictation off": Function(dictation_off),
        "say <text>": Text("%(text)s"),
        # Ego
        "show dragon tip": Text(""),
        "move dragon tip": Mouse("[15, 8]/200, left:down, [0.66, 0.98], left:up, <-50,0>"),
    },
    namespace={
        "Key": Key,
        "Text": Text,
    }
)

class KeystrokeRule(MappingRule):
    exported = False
    mapping = grammarCfg.cmd.map
    extras = [
        IntegerRef("n", 1, 100),
        IntegerRef("m", 0, 100),
        Dictation("text"),
        Dictation("text2"),
        Choice("formatType", formatMap),
        Choice("abbreviation", abbreviationMap),
        Choice("reservedWord", reservedWord),
    ]
    defaults = {
        "n": 1,
        "m": 0,
    }

alternatives = []
alternatives.append(RuleRef(rule=KeystrokeRule()))
single_action = Alternative(alternatives)

sequence = Repetition(single_action, min=1, max=16, name="sequence")

class RepeatRule(CompoundRule):
    # Here we define this rule's spoken-form and special elements.
    spec = "<sequence> [[[and] repeat [that]] <n> times]"
    extras = [
        sequence,  # Sequence of actions defined above.
        IntegerRef("n", 1, 100),  # Times to repeat the sequence.
    ]
    defaults = {
        "n": 1,  # Default repeat count.
    }

    def _process_recognition(self, node, extras):  # @UnusedVariable
        sequence = extras["sequence"]  # A sequence of actions.
        count = extras["n"]  # An integer repeat count.
        for i in range(count):  # @UnusedVariable
            for action in sequence:
                action.execute()
        release.execute()
 
class KeysOnlyRule(MappingRule):
    exported = False
    mapping = {k:Key(v) for k,v in lib.mappings.keys.items()}
    mapping.update({"<formatType> <text>": Function(format_text)})
    # mapping.update({"sh":Mouse("<0,0>,left")})
    extras = [
        Dictation("text"),
        Choice("formatType", formatMap),
        IntegerRef("n", 1, 100),  # Times to repeat the sequence.
    ]
    defaults = {
        "n":1,
    }

class LiteralRule(MappingRule):
    exported = False
    mapping = {
        # "paste":Text("paste!"),
        "<text>": Text("%(text)s"),
    }
    extras = [
        Dictation("text"),
    ]
    defaults = {
    }

class SayRule(MappingRule):
    exported = False
    mapping = {k:Key(v) for k,v in lib.mappings.sayablePunctuation.items()}
    mapping.update({"<text>":Text("%(text)s")})
    extras=[
        Dictation("text"),
    ]
    defaults = {}

class NumberRule(MappingRule):
    exported = False
    mapping = {k:Key(v) for k,v in lib.mappings.digits.items()}
    extras=[
    ]
    defaults = {}

def bringDynamic(text):
    print text
    BringApp(text+"").execute()

class BringMeRule(MappingRule):
    exported = False
    mapping = {}
    mapping.update({"<text>":Function( lambda text: bringDynamic(text) )})
    extras=[
        Dictation("text"),
    ]
    defaults = {}
    
def makePrefixedCompoundRule(prefix,mappingRule):
    alts = []
    alts.append(RuleRef(rule=mappingRule()))
    singleAction = Alternative(alts)
    seq = Repetition(singleAction, min=1, max=16, name="mySequence")
    class PrefixCompoundRule(CompoundRule):
        spec = prefix+" <mySequence>"
        extras = [
            seq
        ]
        defaults = {
        }
        def _process_recognition(self, node, extras):
            sequence = extras["mySequence"]
            for action in sequence:
                action.execute()
            release.execute()
    dynamicName = "Prefix"+prefix+"Rule"
    PrefixCompoundRule.__name__ = dynamicName
    PrefixCompoundRule.__qualname__ = dynamicName
    return PrefixCompoundRule
###############################################################
PrefixKeyRule = makePrefixedCompoundRule("",KeysOnlyRule)
PrefixLiteralRule = makePrefixedCompoundRule("literal",LiteralRule)
PrefixSayRule = makePrefixedCompoundRule("say",SayRule)
PrefixBringRule = makePrefixedCompoundRule("switch to",BringMeRule)
PrefixNumberRule = makePrefixedCompoundRule("number",NumberRule)

grammar = Grammar("Generic edit")
grammar.add_rule(PrefixKeyRule())  # Add the top-level rule.
grammar.add_rule(PrefixLiteralRule())
grammar.add_rule(PrefixSayRule())
grammar.add_rule(PrefixBringRule())

grammar.load()  # Load the grammar.

def unload():
    """Unload function which will be called at unload time."""
    global grammar
    if grammar:
        grammar.unload()
    grammar = None


################################################################################
# def disable():
#     grammar.disable()
# def enableDictation():
#     grammar.enable()


