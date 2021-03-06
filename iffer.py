import util

class If(object):
    def __init__(self, number):
        self.number = number
        self.top = []
        self.bottom = []
        self.lines_consumed = 0
        self.state = 'if'
        self.nested_ifs = -1

    def add_line(self, line):
        self.lines_consumed += 1

        if util.real_strip(line) == 'if':
            self.nested_ifs += 1

        if util.real_strip(line) == 'fi':
            if self.nested_ifs == 0:
                return False

        if self.state == 'if':
            self.state = 'top'
            return True

        if self.state == 'top':
            if util.real_strip(line) == 'else':
                if self.nested_ifs == 0:
                    self.state = 'bottom'
                    return True
            self.top.append(util.real_strip(line))
            if util.real_strip(line) == 'fi':
              self.nested_ifs -= 1
            return True

        if self.state == 'bottom':
            self.bottom.append(util.real_strip(line))
            if util.real_strip(line) == 'fi':
              self.nested_ifs -= 1
            return True

        if util.real_strip(line) == 'fi':
            self.nested_ifs -= 1

        return True

    def select_statement(self):
        select = "SEL @__if_statement_{0}@ @__else_statement_{0}@"
        return select.format(self.number)

    def to_extend(self):
        top_label = '@__if_statement_{0}@'.format(self.number)
        bottom_label = '@__else_statement_{0}@'.format(self.number)
        top_code = [top_label] + self.top + ['JOIN']
        bottom_code = [bottom_label] + self.bottom + ['JOIN']
        return top_code + bottom_code

class Iffer(object):
    def __init__(self, lines, counter=0):
        self.lines = lines
        self.ifs = []
        self.counter = counter

    def is_if_statement(self, ll):
        if ll.strip() == 'if':
            return True
        else:
            return False

    def consume_if(self, linenumber):
        iffy = If(self.counter)
        self.counter += 1
        idx = linenumber
        while iffy.add_line(self.lines[idx]):
            idx += 1
        self.ifs.append(iffy)
        return iffy.select_statement(), iffy.lines_consumed

    def parse(self):
        out = []
        num_lines = 0
        for xx, ll in enumerate(self.lines):
            if self.is_if_statement(ll) and num_lines == 0:
                modline, num_lines = self.consume_if(xx)
                out.append(modline)
                num_lines -= 1
            else:
                if num_lines > 0:
                    num_lines -= 1
                else:
                    out.append(ll)

        ifs = len(self.ifs)
        new_ifs = None

        while new_ifs != 0:
            new_ifs = 0
            for iffy in self.ifs:
                newIffer = Iffer(iffy.top, self.counter)
                newIffer.parse()
                if len(newIffer.ifs) > 0:
                    self.counter += len(newIffer.ifs)
                    self.ifs.extend(newIffer.ifs)
                    iffy.top = newIffer.lines
                    new_ifs += len(newIffer.ifs)

            for iffy in self.ifs:
                newIffer = Iffer(iffy.bottom, self.counter)
                newIffer.parse()
                if len(newIffer.ifs) > 0:
                    self.counter += len(newIffer.ifs)
                    self.ifs.extend(newIffer.ifs)
                    iffy.bottom = newIffer.lines
                    new_ifs += len(newIffer.ifs)

        self.lines = out
