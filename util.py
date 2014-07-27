import re

def filter_lines(lines):
    out = []
    for ll in lines:
        if ll.strip() == '':
            continue
        else:
            out.append(ll.strip())
    return out

def real_strip(line):
    line = re.sub(r';.*', '', line)
    return line.strip()
