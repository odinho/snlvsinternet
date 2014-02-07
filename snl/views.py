from django.shortcuts import render

from snl.models import Article
from texttools.utils import KeywordFinder

SNL_URL = 'http://snl.no/{key}'

def show(request, snl_key):
    article = Article.objects.fetch(
                  SNL_URL.format(key=snl_key))
    kf = KeywordFinder()
    keywords = kf.find_keywords_and_freqs(article.xhtml_body)
    return render(request, 'snl/show.html', {
        'article': article,
        'keywords': keywords,
    })
