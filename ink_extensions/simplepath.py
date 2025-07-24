"""
simplepath.py
functions for digesting paths into a simple list structure

Copyright (C) 2005 Aaron Spike, aaron@ekips.org

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""
import re
import math

RE_DELIM = re.compile(r'[ \t\r\n,]+')
RE_COMMAND = re.compile(r'[MLHVCSQTAZmlhvcsqtaz]')
RE_PARAMETER = re.compile(r'(([-+]?[0-9]+(\.[0-9]*)?|[-+]?\.[0-9]+)([eE][-+]?[0-9]+)?)')

# The following constants taken from inkex module from Inkscape 1.2:
LEX_REX = re.compile(r"([MLHVCSQTAZmlhvcsqtaz])([^MLHVCSQTAZmlhvcsqtaz]*)")

DIGIT_REX_PART = r"[0-9]"
DIGIT_SEQUENCE_REX_PART = rf"(?:{DIGIT_REX_PART}+)"
INTEGER_CONSTANT_REX_PART = DIGIT_SEQUENCE_REX_PART
SIGN_REX_PART = r"[+-]"
EXPONENT_REX_PART = rf"(?:[eE]{SIGN_REX_PART}?{DIGIT_SEQUENCE_REX_PART})"
FRACTIONAL_CONSTANT_REX_PART =\
    rf"(?:{DIGIT_SEQUENCE_REX_PART}?\.{DIGIT_SEQUENCE_REX_PART}|{DIGIT_SEQUENCE_REX_PART}\.)"
FLOATING_POINT_CONSTANT_REX_PART = rf"(?:{FRACTIONAL_CONSTANT_REX_PART}{EXPONENT_REX_PART}?|{DIGIT_SEQUENCE_REX_PART}{EXPONENT_REX_PART})"
NUMBER_REX = re.compile(
    rf"(?:{SIGN_REX_PART}?{FLOATING_POINT_CONSTANT_REX_PART}|{SIGN_REX_PART}?{INTEGER_CONSTANT_REX_PART})"
)


def lexPath(d):
    """
    returns and iterator that breaks path data
    identifies command and parameter tokens

    Note: This function no longer in use by parsePath (the only
    function that used it), but is left here in case any outside
    software does make use of it.
    """
    offset = 0
    length = len(d)

    while 1:
        m = RE_DELIM.match(d, offset)
        if m:
            offset = m.end()
        if offset >= length:
            break
        m = RE_COMMAND.match(d, offset)
        if m:
            yield [d[offset:m.end()], True]
            offset = m.end()
            continue
        m = RE_PARAMETER.match(d, offset)
        if m:
            yield [d[offset:m.end()], False]
            offset = m.end()
            continue
        #TODO: create new exception
        raise Exception('Invalid path data!')


IMPLICIT_NEXT_CMDS = {
    'M': 'L',
    'm': 'l',
    'L': 'L',
    'l': 'l',
    'H': 'H',
    'h': 'h',
    'V': 'V',
    'v': 'v',
    'C': 'C',
    'c': 'c',
    'S': 'S',
    's': 's',
    'Q': 'Q',
    'q': 'q',
    'T': 'T',
    't': 't',
    'A': 'A',
    'a': 'a',
    'Z': 'L',
    'z': 'l'
    }


def parse_string(path_d):
    """
    Parse path string into commands and parameters.
    Replaces lexPath (with changes made to parsePath).
    Based on parse_string() in inkex from Inkscape 1.2.
    """
    for cmd, numbers in LEX_REX.findall(path_d):
        args = [float(val) for val in NUMBER_REX.findall(numbers)]
        numParams = pathdefs[cmd.upper()][1]
        next_cmd = IMPLICIT_NEXT_CMDS[cmd]
        i = 0
        while i < len(args) or numParams == 0:
            if len(args[i: i + numParams]) != numParams:
                return
            yield cmd, args[i: i + numParams]
            i += numParams
            cmd = next_cmd
            numParams = pathdefs[cmd.upper()][1]


def parse_string2(path_d):
    """
    Parse SVG path string using ASCII command encoding and pre-computed lookups.
    Returns (ascii_cmd, args) tuples for internal processing.
    """
    for cmd_str, numbers in LEX_REX.findall(path_d):
        args = [float(val) for val in NUMBER_REX.findall(numbers)]
        args_len = len(args)  # Cache length

        # Convert to ASCII directly
        cmd_ascii = ord(cmd_str)

        # Direct O(1) lookups using pre-computed tables
        numParams = CMD_PARAM_COUNTS[cmd_ascii]
        next_cmd_ascii = CMD_NEXT_CMDS[cmd_ascii]

        i = 0
        while i < args_len or numParams == 0:
            # Bounds check
            if i + numParams > args_len:
                return

            # Yield ASCII command with args
            yield cmd_ascii, args[i: i + numParams]
            i += numParams
            cmd_ascii = next_cmd_ascii

            # Direct lookup in loop (no list indexing)
            numParams = CMD_PARAM_COUNTS[cmd_ascii]


'''
pathdefs = {commandfamily:
    [
    implicitnext,
    #params,
    [casts,cast,cast],
    [coord type,x,y,0]
    ]}
'''
pathdefs = {
    'M': ['L', 2, [float, float], ['x', 'y']],
    'L': ['L', 2, [float, float], ['x', 'y']],
    'H': ['H', 1, [float], ['x']],
    'V': ['V', 1, [float], ['y']],
    'C': ['C', 6, [float, float, float, float, float, float], ['x', 'y', 'x', 'y', 'x', 'y']],
    'S': ['S', 4, [float, float, float, float], ['x', 'y', 'x', 'y']],
    'Q': ['Q', 4, [float, float, float, float], ['x', 'y', 'x', 'y']],
    'T': ['T', 2, [float, float], ['x', 'y']],
    'A': ['A', 7,
          [float, float, float, int, int, float, float], ['r', 'r', 'a', 0, 's', 'x', 'y']],
    'Z': ['L', 0, [], []]
    }


# ASCII-based command encoding for efficient processing
# Using ASCII values directly: 'A'=65, 'a'=97, etc.
# Uppercase (absolute) commands: 65-90, Lowercase (relative) commands: 97-122
# Enables relative detection: cmd > 96
# Direct conversion available: chr(cmd) gives the letter

# Format: {ascii_code: [next_ascii_code, param_count, [cast_funcs], [coord_types]]}
pathdefs_numeric = {
    77: [76, 2, [float, float], ['x', 'y']],     # 'M' -> 'L'
    109: [108, 2, [float, float], ['x', 'y']],   # 'm' -> 'l'
    76: [76, 2, [float, float], ['x', 'y']],     # 'L' -> 'L'
    108: [108, 2, [float, float], ['x', 'y']],   # 'l' -> 'l'
    72: [72, 1, [float], ['x']],                 # 'H' -> 'H'
    104: [104, 1, [float], ['x']],               # 'h' -> 'h'
    86: [86, 1, [float], ['y']],                 # 'V' -> 'V'
    118: [118, 1, [float], ['y']],               # 'v' -> 'v'
    67: [67, 6, [float, float, float, float, float, float], ['x', 'y', 'x', 'y', 'x', 'y']],  # 'C'
    99: [99, 6, [float, float, float, float, float, float], ['x', 'y', 'x', 'y', 'x', 'y']],  # 'c'
    83: [83, 4, [float, float, float, float], ['x', 'y', 'x', 'y']],     # 'S' -> 'S'
    115: [115, 4, [float, float, float, float], ['x', 'y', 'x', 'y']],   # 's' -> 's'
    81: [81, 4, [float, float, float, float], ['x', 'y', 'x', 'y']],     # 'Q' -> 'Q'
    113: [113, 4, [float, float, float, float], ['x', 'y', 'x', 'y']],   # 'q' -> 'q'
    84: [84, 2, [float, float], ['x', 'y']],     # 'T' -> 'T'
    116: [116, 2, [float, float], ['x', 'y']],   # 't' -> 't'
    65: [65, 7, [float, float, float, int, int, float, float],
         ['r', 'r', 'a', 0, 's', 'x', 'y']],  # 'A'
    97: [97, 7, [float, float, float, int, int, float, float],
         ['r', 'r', 'a', 0, 's', 'x', 'y']],  # 'a'
    90: [76, 0, [], []],                         # 'Z' -> 'L'
    122: [108, 0, [], []]                        # 'z' -> 'l'
}

# Pre-computed lookup tables for efficient processing
CMD_PARAM_COUNTS = {ascii_val: pathdef[1] for ascii_val, pathdef in pathdefs_numeric.items()}
CMD_NEXT_CMDS = {ascii_val: pathdef[0] for ascii_val, pathdef in pathdefs_numeric.items()}

LOWER_CMDS = set(['m', 'l', 'h', 'v', 'c', 's', 'q', 't', 'a', 'z'])


def parsePath(d):
    """
    Parse SVG path and return an array of segments.
    Removes all shorthand notation.
    Converts coordinates to absolute.
    """
    retval = []
    lexer = parse_string(d)

    pen = (0.0, 0.0)
    subPathStart = pen
    lastControl = pen
    lastCommand = ''

    while 1:
        try:
            cmd, args = next(lexer)
        except StopIteration:
            break
        cmd_upper = cmd.upper()
        if not lastCommand and cmd_upper != 'M':
            raise Exception('Invalid path, must begin with moveto.')

        numParams = pathdefs[cmd_upper][1]
        params = []

        for index, value in enumerate(args):
            cast = pathdefs[cmd_upper][2][index]
            param = cast(value)
            if cmd in LOWER_CMDS:
                if pathdefs[cmd_upper][3][index] == 'x':
                    param += pen[0]
                elif pathdefs[cmd_upper][3][index] == 'y':
                    param += pen[1]
            params.append(param)
        outputCommand = cmd_upper  # Since parameters are now absolute

        # Flesh out shortcut notation
        if outputCommand in ('H', 'V'):
            if outputCommand == 'H':
                params.append(pen[1])
            if outputCommand == 'V':
                params.insert(0, pen[0])
            outputCommand = 'L'
        if outputCommand in ('S', 'T'):
            params.insert(0, pen[1]+(pen[1]-lastControl[1]))
            params.insert(0, pen[0]+(pen[0]-lastControl[0]))
            if outputCommand == 'S':
                outputCommand = 'C'
            if outputCommand == 'T':
                outputCommand = 'Q'

        # current values become "last" values
        if outputCommand == 'M':
            subPathStart = tuple(params[0:2])
            pen = subPathStart
        if outputCommand == 'Z':
            pen = subPathStart
        else:
            pen = tuple(params[-2:])

        if outputCommand in ('Q', 'C'):
            lastControl = tuple(params[-4:-2])
        else:
            lastControl = pen
        lastCommand = cmd_upper

        retval.append([outputCommand, params])
    return retval


def parsePath2(d):
    """
    Parse SVG path string using ASCII encoding throughout.
    Uses integer comparisons for efficient command processing.
    Maintains backward compatibility with string commands in output.
    """
    retval = []
    lexer = parse_string2(d)  # Use ASCII parser

    pen = (0.0, 0.0)
    subPathStart = pen
    lastControl = pen
    lastCommand = 0  # Store as ASCII code instead of string

    while 1:
        try:
            cmd_ascii, args = next(lexer)
        except StopIteration:
            break

        # ASCII uppercase conversion using bit manipulation
        cmd_upper_ascii = cmd_ascii & ~32 if cmd_ascii > 96 else cmd_ascii

        if not lastCommand and cmd_upper_ascii != 77:  # 77 = 'M'
            raise Exception('Invalid path, must begin with moveto.')

        # Use ASCII pathdef lookup
        pathdef = pathdefs_numeric[cmd_ascii]
        params = []

        for index, value in enumerate(args):
            cast = pathdef[2][index]
            param = cast(value)
            # Relative check: cmd_ascii > 96 means lowercase
            if cmd_ascii > 96:
                if pathdef[3][index] == 'x':
                    param += pen[0]
                elif pathdef[3][index] == 'y':
                    param += pen[1]
            params.append(param)

        # Convert to string only for output compatibility
        outputCommand = chr(cmd_upper_ascii)

        # Flesh out shortcut notation using ASCII comparisons
        if cmd_upper_ascii == 72 or cmd_upper_ascii == 86:  # 'H'=72, 'V'=86
            if cmd_upper_ascii == 72:  # 'H'
                params.append(pen[1])
            else:  # 'V'
                params.insert(0, pen[0])
            outputCommand = 'L'
            cmd_upper_ascii = 76  # 'L'=76
        elif cmd_upper_ascii == 83 or cmd_upper_ascii == 84:  # 'S'=83, 'T'=84
            params.insert(0, pen[1]+(pen[1]-lastControl[1]))
            params.insert(0, pen[0]+(pen[0]-lastControl[0]))
            if cmd_upper_ascii == 83:  # 'S'
                outputCommand = 'C'
                cmd_upper_ascii = 67  # 'C'=67
            else:  # 'T'
                outputCommand = 'Q'
                cmd_upper_ascii = 81  # 'Q'=81

        # Current values become "last" values - ASCII comparisons
        if cmd_upper_ascii == 77:  # 'M'=77
            subPathStart = tuple(params[0:2])
            pen = subPathStart
        elif cmd_upper_ascii == 90:  # 'Z'=90
            pen = subPathStart
        else:
            pen = tuple(params[-2:])

        if cmd_upper_ascii == 81 or cmd_upper_ascii == 67:  # 'Q'=81, 'C'=67
            lastControl = tuple(params[-4:-2])
        else:
            lastControl = pen
        lastCommand = cmd_upper_ascii

        retval.append([outputCommand, params])
    return retval


def formatPath(a):
    """Format SVG path data from an array"""
    return "".join([cmd + " ".join([str(p) for p in params]) for cmd, params in a])


def translatePath(p, x, y):
    for cmd, params in p:
        defs = pathdefs[cmd]
        for i in range(defs[1]):
            if defs[3][i] == 'x':
                params[i] += x
            elif defs[3][i] == 'y':
                params[i] += y


def scalePath(p, x, y):
    for cmd, params in p:
        defs = pathdefs[cmd]
        for i in range(defs[1]):
            if defs[3][i] == 'x':
                params[i] *= x
            elif defs[3][i] == 'y':
                params[i] *= y
            elif defs[3][i] == 'r':         # radius parameter
                params[i] *= x
            elif defs[3][i] == 's':         # sweep-flag parameter
                if x*y < 0:
                    params[i] = 1 - params[i]
            elif defs[3][i] == 'a':         # x-axis-rotation angle
                if y < 0:
                    params[i] = - params[i]


def rotatePath(p, a, cx=0, cy=0):
    if a == 0:
        return p
    for cmd, params in p:
        defs = pathdefs[cmd]
        for i in range(defs[1]):
            if defs[3][i] == 'x':
                x = params[i] - cx
                y = params[i + 1] - cy
                r = math.sqrt((x**2) + (y**2))
                if r != 0:
                    theta = math.atan2(y, x) + a
                    params[i] = (r * math.cos(theta)) + cx
                    params[i + 1] = (r * math.sin(theta)) + cy


# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
