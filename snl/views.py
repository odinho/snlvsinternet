from django.shortcuts import render
from snl.models import Article

SNL_URL = 'http://snl.no/{key}'

def show(request, snl_key):
    article = Article.objects.fetch(
                  SNL_URL.format(key=snl_key))
    return render(request, 'snl/show.html', {'article': article})
