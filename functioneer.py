import inspect
import re

class Funct(object):

    def __init__(self, name, args, lines):
        self.name = name
        self.args = args
        self.lines = lines

    def add_line(self, line):
        self.lines.append(line)

    def is_fn_call(self, line):
        return re.match(r'(.*)\((.*)\)', line) is not None

    def parse_calls(self):
        """Transform any function calls like do_x(arg1, arg2) into assembly
        """
        for xx, ll in enumerate(self.lines):
            if self.is_fn_call(ll):
                self.lines[xx] = FuncCall(ll).parse()
        out = []
        for ll in self.lines:
            if isinstance(ll, basestring):
               out.append(ll)
            else:
                out.extend(ll)
        self.lines = out

    def output(self):
        self.parse_calls()
        out = self.lines
        out.insert(0, ':' + self.name + ':')
        out.append('RTN')
        return "\n".join(out)

    def __repr__(self):
        msg = "[Name: {0}, Args: {1}, Lines: {2}]"
        return msg.format(self.name, self.args, self.lines)


class FuncCall(object):

    def __init__(self, call):
        self.call = call

    def parse(self):
        sre = re.match(r'(.*)\((.*)\)', self.call)
        fn_name = sre.group(1)
        args = sre.group(2)
        if args == "":
            args = "0"
        return ['LDF :' + fn_name + ':', 'AP ' + args]


class Functioneer(object):

    def __init__(self, lines):
        self.lines = lines
        self.fns = []

    def get_functions(self):
        fn = None
        for ll in self.lines:
            if ll[0:3] == 'def':
                if fn:
                    self.fns.append(fn)
                fn = Funct(name=ll.split(' ')[1],
                           args=int(ll.split(' ')[2]),
                           lines=[])
            else:
                if ll.strip() != '':
                    fn.add_line(ll.strip())
        self.fns.append(fn)

    def index_of(self, name):
        for xx, fn in enumerate(self.fns):
            if fn.name == name:
                return xx
        return -1
