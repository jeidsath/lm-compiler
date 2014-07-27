import re
import util


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
        self.loadMacros()

        for mm in self.macros:
            newText = []
            for ll in self.text:
                newText.append(ll.replace(mm[0], "\n".join(mm[1:])))
            self.text = newText

        return self.text
