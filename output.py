import re

class Outputer(object):
    def __init__(self, functioneer, iffer):
        self.iffer = iffer
        self.functioneer = functioneer

    def labelled_text(self):
        full_text = "\n".join([fn.output() for fn in self.functioneer.fns])
        return full_text.split('\n')

    def replaceFn(self, lines):
        changed = False
        for xx, ll in enumerate(lines):
            mm = re.match(r'^:(.*):', ll)
            if mm:
                lines = self.replace(mm.group(1), lines)
                changed = True
        return lines, changed

    def replace(self, name, lines):
        fn_addr = -1
        for xx, ll in enumerate(lines):
            if ll == ':' + name + ':':
                fn_addr = xx
        lines.remove(':' + name + ':')
        for xx, ll in enumerate(lines):
            lines[xx] = ll.replace(':' + name + ':', str(fn_addr))
        return lines

    def out(self):
        text = self.labelled_text()

        for iffy in self.iffer.ifs:
            text.extend(iffy.to_extend())

        while True:
            text, changed = self.replaceFn(text)
            if not changed:
                break

        return "\n".join(text)
