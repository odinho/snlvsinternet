from django.test import TestCase

from wikipedia.models import WikipediaArticle

class LiveURLFetch(TestCase):
    def test_live_fetch_article_from_api(self):
        a = WikipediaArticle.objects._fetch_from_api('Oslo')
        self.assertEqual(a['title'], 'Oslo')

    def test_live_article_fetch(self):
        a = WikipediaArticle.objects.fetch('Oslo')
        self.assertEqual(a.key, 'Oslo')
