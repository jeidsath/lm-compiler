import re

class Commenter(object):
    def __init__(self, text):
        self.text = text

    def comments_removed(self):
        out = []

        for line in self.text:
            out.append(re.sub('#(.*)', r';\1', line))

        return out
