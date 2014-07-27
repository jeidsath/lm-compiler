import re
import util
import subprocess
import sys
from StringIO import StringIO


class Macroer(object):
    def __init__(self, text, macrosFile):
        self.text = text
        self.macrosFile = macrosFile
        self.macros = []

    def loadMacros(self):
        with open(self.macrosFile, 'r') as ff:
            text = ff.readlines()

        macro = []
        for ll in text:
            mm = re.match(r'^DEFINE (.*)$', ll)
            if mm:
                if len(macro) > 0:
                    self.macros.append(macro)
                macro = [util.real_strip(mm.group(1))]
            else:
                stripped = util.real_strip(ll)
                if stripped != '':
                    macro.append(stripped)
        if len(macro) > 0:
            self.macros.append(macro)

    def replaceMacros(self):
        self.replacePrograms()

        self.loadMacros()

        for mm in self.macros:
            newText = []
            for ll in self.text:
                newText.append(ll.replace(mm[0], "\n".join(mm[1:])))
            self.text = newText


        return self.text

    def replacePrograms(self):
        idx, block = self.get_block()
        while idx:
            output = self.execute_block(block)
            self.replace_block(idx, len(block) + 2, output)
            idx, block = self.get_block()

    def get_block(self):
        start = None
        end = None
        for xx, ll in enumerate(self.text):
            if not start:
                if util.real_strip(ll) == '<$':
                    start = xx
            if not end:
                if util.real_strip(ll) == '$>':
                    end = xx
        if start:
            return start, self.text[start + 1:end]
        else:
            return None, None

    def execute_block(self, block):
        buffer = StringIO()
        sys.stdout = buffer
        exec "\n".join(block)
        sys.stdout = sys.__stdout__
        return buffer.getvalue()

    def replace_block(self, idx, size, replacement):
        self.text = self.text[0:idx] + replacement.split("\n") + self.text[idx + size:]
