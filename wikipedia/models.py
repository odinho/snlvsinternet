import requests
from django.db import models

class WikipediaArticleManager(models.Manager):
    def _fetch_from_api(self, key):
        api_url = u'http://no.wikipedia.org/w/api.php?action=parse&page={key}&format=json&prop=text'.format(key=key)
        resp = requests.get(api_url.encode('utf-8'))
        return resp.json()['parse']

    def fetch(self, key):
        try:
            return WikipediaArticle.objects.get(key=key)
        except WikipediaArticle.DoesNotExist:
            article = self._fetch_from_api(key)
            wa = WikipediaArticle(key=key, html_body=article['text']['*'])
            wa.save()
            return wa

class WikipediaArticle(models.Model):
    key = models.CharField(max_length=120, unique=True)
    html_body = models.TextField()

    objects = WikipediaArticleManager()
