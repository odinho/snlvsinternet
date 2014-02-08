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
    snl_keywords = kf.find_keywords_and_freqs(snl.xhtml_body)
    kf.add_stopwords_from_file(settings.WIKIPEDIA_STOPWORD_FILE)
    wp_keywords = kf.find_keywords_and_freqs(wp.html_body)
    return render(request, 'snl/vs.html', {
        'snl_kw': snl_keywords,
        'wp_kw': wp_keywords,
        'snl': snl,
        'wp': wp,
    })
