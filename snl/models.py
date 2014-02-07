import requests
from django.db import models
from jsonfield import JSONField

#SNL_URL = 'http://snl.no/{key}.json'

class ArticleManager(models.Manager):
    def _fetch_article_from_api(self, url):
        api_url = '{url}.json'.format(url=url)
        resp = requests.get(api_url)
        return resp.json()

    def create_article_from_dict(self, article_dict):
        author_list = article_dict.pop('authors')
        images = article_dict.pop('images')
        a = Article(**article_dict)
        a.save()
        for author in author_list:
            author_obj, created = Author.objects.get_or_create(
                                full_name=author['full_name'])
            a.authors.add(author_obj)
        for image in images:
            a.images.create(**image)
        a.save()
        return a

    def fetch(self, url):
        try:
            return Article.objects.get(url=url)
        except Article.DoesNotExist:
            article_dict = self._fetch_article_from_api(url)
            return self.create_article_from_dict(article_dict)

class Article(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=120)
    subject_title = models.CharField(max_length=120)
    subject_url = models.URLField()
    changed_at = models.DateTimeField()
    created_at = models.DateTimeField()
    metadata = JSONField()
    xhtml_body = models.TextField()
    license_name = models.CharField(max_length=16)
    metadata_license_name = models.CharField(max_length=16)

    authors = models.ManyToManyField('Author')

    objects = ArticleManager()


class Author(models.Model):
    full_name = models.CharField(max_length=100, unique=True)

class Image(models.Model):
    full_size_url = models.URLField(unique=True)
    standard_size_url = models.URLField()
    heading = models.CharField(max_length=100)
    license = models.CharField(max_length=100)
    xhtml = models.TextField()
    copyright = models.CharField(max_length=100)
    paragraph_index = models.IntegerField()
    type = models.CharField(max_length=32)

    article = models.ForeignKey(Article, related_name='images')
