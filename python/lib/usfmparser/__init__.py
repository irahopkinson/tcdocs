#!/usr/bin/python3

import os, argparse, logging, re
from .fparser import createParser, make_tokenizer, debug_print
from .funcparserlib import parser as fpp
from .funcparserlib.parser import some, finished
from .funcparserlib.lexer import Token
from .usxmodel import usx, char, para

class UsfmParser:
    _tokenspecs = [
        ('EndTag',      (r"\\(?P<embed>\+?)(?P<tname>[a-z][a-z0-9]*)?\*", )),
        ('Tag',         (r"\\(?P<embed>\+?)(?P<tname>[a-z][a-z0-9]*)(?:\s|(?!\*))", )),
        ('Attribute',   (r"(?P<key>[a-z][a-z0-9]*)\s*=\"(?P<val>.*?)\"\s*", )),
        ('Pipe',        (r"\|", )),
        ('Word',        (r".+?(?=[\\\s]|$)", )),
        ('Ws',          (r"\s", ))
    ]

    def __init__(self):
        self._tags = {}

    def _readstylesheet(self, fname):
        currtag = None
        with open(fname, encoding="utf-8") as inf:
            for l in inf.readlines():
                m = re.match(r"^(?:#!)?\s*\\(\S+)\s*(.*?)$", l.strip())
                if m is None:
                    continue
                mkr = m.group(1)
                val = m.group(2)
                if mkr == "Marker":
                    currtag = val
                    self._tags[currtag] = {}
                else:
                    self._tags[currtag][mkr] = val

    def _tokenize(self, content):
        t = make_tokenizer(self._tokenspecs)
        return list(t(content))

    def _tagtype(self, tag):
        return self._tags.get(tag, {}).get('StyleType', None)

    def TagType(self, test):
        return some(lambda t: t.type == "Tag" and t.embed == "" and self._tagtype(t.tname) == test)

    def EndTag(self):
        return some(lambda t: t.type == "EndTag" and t.embed == "")

    def TagEmbed(self):
        return some(lambda t: t.type == "Tag" and t.embed == "+" and self._tagtype(t.tname) == "Character")

    def EndTagEmbed(self):
        def _tt(t):
            if t.type == 'EndTag':
                return t.embed == "+"
            return False
        return some(_tt)

    def CmpTag(self, opening, ending):
        if opening is None or ending is None:
            return True
        if opening.type != "Tag":
            return False
        if ending.type != "EndTag":
            return False
        if opening.embed != ending.embed:
            return False
        if opening.tname != ending.tname:
            return False
        return True

    def Word(self):
        return some(lambda t: t.type == "Word")

    def Ws(self):
        return some(lambda t: t.type == "Ws")

    def finished(self):
        return finished

    def make_char(self, tag, c1, c2):
        content = []
        # import pdb; pdb.set_trace()
        for c in c1:
            for a in c:
                content.append(a.value if isinstance(a, Token) else a)
        content.append(c2.value if isinstance(c2, Token) else c2)
        return char(attrib={'style': tag.tname}, *content)

    def make_usx(self, c):
        return usx(attrib={"version": "1.0"}, *c)

    def make_para(self, tag, content):
        return para(attrib={'style': tag.tname}, *content)

    def str_join(self, a):
        return "".join(c.value for c in a)

