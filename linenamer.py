import re
import util


class Linenamer(object):

    def __init__(self, lines):
        self.lines = lines
        self.changed = []

    def replace_all(self, ss):
        out = []
        for ll in self.lines:
            out.append(ll.replace(ss, '@' + ss + '@'))
        self.lines = out

    def linesnames_changed(self):
        out = []
        for ll in self.lines:
            if ll[0:8] == 'LINENAME':
                ll = util.real_strip(ll)
                mm = re.match(r'^LINENAME (.*)', ll)
                self.changed.append(mm.group(1))
                out.append(mm.group(1)) # this gets replaced by @ + name + @
            else:
                out.append(ll)
        self.lines = out

        for nn in self.changed:
            self.replace_all(nn)

        return self.lines
