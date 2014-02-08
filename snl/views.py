# -*- encoding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render

from snl.models import Article
from texttools.utils import KeywordFinder
from wikipedia.models import WikipediaArticle

SNL_URL = u'http://snl.no/{key}'

def show(request, snl_key):
    article = Article.objects.fetch(
                  SNL_URL.format(key=snl_key))
    kf = KeywordFinder()
    keywords = kf.find_keywords_and_freqs(article.xhtml_body)
    return render(request, 'snl/show.html', {
        'article': article,
        'keywords': keywords,
    })

def vs(request, snl_key):
    snl = Article.objects.fetch(
                  SNL_URL.format(key=snl_key))
    wp = WikipediaArticle.objects.fetch(key=snl_key)
    kf = KeywordFinder()

    snl_words, snl_wc = kf.get_word_freqs(snl.xhtml_body)

    kf.add_stopwords_from_file(settings.WIKIPEDIA_STOPWORD_FILE)
    wp_words, wp_wc = kf.get_word_freqs(wp.html_body)

    snl_top = sorted(snl_words, key=snl_words.get, reverse=True)[:10]
    wp_top = sorted(wp_words, key=wp_words.get, reverse=True)[:10]

    all_words = {}
    for w in set(snl_words) | set(wp_words):
        if w in snl_top or w in wp_top:
            continue
        all_words[w] = snl_words.get(w, 0) + wp_words.get(w, 0)
    all_top = sorted(all_words, key=all_words.get, reverse=True)[:10]

    keywords = set(snl_top + wp_top + all_top)

    return render(request, 'snl/vs.html', {
        'key': snl_key,

        'keywords': keywords,
        'snl_words': snl_words,
        'wp_words': wp_words,

        'snl': snl,
        'wp': wp,
    })
