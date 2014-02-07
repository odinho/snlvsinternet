import htmlentitydefs
import re
from collections import defaultdict
from django.utils.html import strip_tags
from django.conf import settings

class KeywordFinder(object):
    def __init__(self):
        with open(settings.STOPWORD_FILE) as f:
            self.stopword_set = frozenset(f.readlines())

    def find_keywords(self, text):
        sanitised_text = strip_tags(unescape(text)).lower()
        word_count = defaultdict(int)
        delim = re.compile(r'[^\w]')

        for word in delim.split(sanitised_text):
            if word:
                word_count[word] += 1

        sorted_list = sorted(word_count, key=word_count.get, reverse=True)
        return sorted_list[:10]

def find_keywords(text):
    return KeywordFinder().find_keywords(text)

def unescape(text):
    '''
    Removes HTML character references and entities from a text string.

    Taken from http://effbot.org/zone/re-sub.htm#unescape-html

    @param text The HTML (or XML) source text.
    @return The plain text, as a Unicode string, if necessary.
    '''
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)
