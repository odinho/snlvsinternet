import operator
import codecs
import htmlentitydefs
import re
from collections import defaultdict
from django.conf import settings
from django.utils.html import strip_tags

class KeywordFinder(object):
    def __init__(self, stopword_fn=settings.STOPWORD_FILE):
        self.stopword_set = frozenset()
        if stopword_fn:
            self.add_stopwords_from_file(stopword_fn)

    def add_stopwords_from_file(self, stopword_fn):
        with codecs.open(stopword_fn, 'r', 'utf-8') as f:
            self.stopword_set |= frozenset(f.read().splitlines())

    def find_keywords(self, text):
        return [w[0] for w in self.find_keywords_and_freqs(text)]

    def sanitize(self, text):
        sanitized_text = strip_tags(unescape(text)).lower()
        return sanitized_text

    def count_word(self, word):
        if word in self.stopword_set:
            return False
        if not word:
            return False
        if word.isdigit():
            if 1000 < int(word):
                return True
            else:
                return False
        return True

    def find_keywords_and_freqs(self, text):
        sanitised_text = self.sanitize(text)
        word_count = defaultdict(int)
        delim = re.compile(r'[^\w]', flags=re.UNICODE)

        for word in delim.split(sanitised_text):
            if not self.count_word(word):
                continue
            word_count[word] += 1
        sorted_list = sorted(word_count.iteritems(),
                             key=operator.itemgetter(1),
                             reverse=True)
        return sorted_list[:10]


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
