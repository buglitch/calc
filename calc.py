#!/usr/bin/env python3
import logging
import os
import re
import readline
import sys
import types

import numbers
import math
import cmath
import decimal as decimals
import fractions
import random as randoms
import statistics

from numbers import *
from math import *
from cmath import *
from decimal import *
from fractions import *
from random import *
from statistics import *

false = False
no = False
true = True
yes = True
nil = None
none = None
null = None
undefined = None
i = j
j = 1j
infi = infj
nani = nanj
phi = (1 + sqrt(5)) / 2

ENV = os.environ.copy()

for k, v in list(globals().items()):
    if not "__" in k and not k.isupper() and not k.islower():
        if not k.lower() in globals():
            globals()[k.lower()] = v

for n in dir(math):
    if "__" in n:
        continue
    elif n in dir(cmath) and isinstance(getattr(math, n), types.BuiltinFunctionType):
        globals()[n] = lambda *x, n=n: (lambda r=getattr(cmath, n)(*x): r.real if r.imag == 0 else r)()

del k
del v
del n

try:
    while True:
        calc = input("\033[95m> \033[39m").strip()
        if calc == "" or calc[0] == "#":
            if re.match("^#[0-9A-Fa-f]{6}$", calc):
                rgb = tuple(int(calc[1:][i:i+2], 16) for i in (0, 2, 4))
                if re.match("(truecolor|24bit|unknown)", os.environ.get("COLORTERM") if os.environ.get("COLORTERM") else "unknown"):
                    print("color: \x1b[48;2;{0[0]};{0[1]};{0[2]}m   \033[0m".format(rgb), end="\t")
                print("tuple: {0}\t rgb: {1[0]}% {1[1]}% {1[2]}%".format(rgb, tuple(int((i / 0xff) * 100) for i in rgb)))
            continue
        elif (calc == "exit()"
            or calc == "exit"
            or calc == "quit()"
            or calc == "quit"
            or calc == "q"
            or calc == ":q"):
            exit()
        try:
            calc = re.sub(r'([0-9]+)i', r'\1j', calc)
            calc = calc.replace('decimal.', 'decimals.')
            calc = calc.replace('random.', 'randoms.')
            try:
                res = eval(calc, globals(), globals())
            except SyntaxError:
                exec(calc, globals(), globals())
                print("ok")
                continue
            except Exception:
                try:
                    res = eval(calc.lower(), globals(), globals())
                except SyntaxError:
                    exec(calc.lower(), globals(), globals())
                    print("ok")
                    continue

            if res == "exit":
                exit()
            else:
                if isinstance(res, complex):
                    if res.imag != 0:
                        print("complex: {0} + {1}i".format(res.real, res.imag))
                        continue
                    else:
                        res = res.real

                if isinstance(res, bool):
                    print("bool: {0}\thex: 0x{0:X}".format(res).lower())
                    continue

                if isinstance(res, float):
                    if isnan(res) or isinf(res) or res != floor(res):
                        print("float: {0:f}".format(res))
                        continue
                    else:
                        res = floor(res)

                if isinstance(res, int):
                    if res != True and res != False:
                        print("dec: {0:d}\thex: 0x{0:X}".format(floor(res)))
                    else:
                        print("dec: {0:d}\thex: 0x{0:X}\tbool: {1}".format(floor(res), bool(floor(res))))
                    continue

                if isinstance(res, types.BuiltinFunctionType):
                    print("python built-in function: {0}".format(res.__name__))
                    continue

                if res == None:
                    print("null")
                    continue

                print("{0}: {1}".format(res.__class__.__name__.lower(), res))
                continue

        except Exception as err:
            func_r = r"^[a-zA-Z_][a-zA-Z0-9_]*"
            if re.match(func_r + r"$", calc) or re.match(func_r + r" ", calc):
                ret = os.system(calc)
                if ret != 0:
                    print("ret: {0:d}\tsig: {1:d}\thex: {0:02X} {1:02X}".format(ret // 0x100, ret % 0x100))
            else:
                print("error: {0}".format(err))

except KeyboardInterrupt:
    print('\033[3m\b keyboard interrupt\033[0m')

except EOFError:
    print('\033[3m\b eof\033[0m')
    exit()
