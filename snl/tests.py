from django.test import TestCase

# Create your tests here.
from snl.models import Article

class LiveURLFetch(TestCase):
    def test_live_fetch_article_from_api(self):
        a = Article.objects._fetch_article_from_api('http://snl.no/Oslo')
        self.assertEqual(a['title'], 'Oslo')

    def test_live_article_fetch(self):
        a = Article.objects.fetch('http://snl.no/Oslo')
        self.assertEqual(a.title, 'Oslo')

class CreateArticle(TestCase):
    def test_create_article_from_dict(self):
        dict_ = {
          "authors": [ { "full_name": "Geir Thorsnes" } ],
          "changed_at": "2013-12-29T13:11:46Z",
          "created_at": "2009-02-14T07:51:18Z",
          "images": [ {
            "copyright": "",
            "full_size_url": "http://media.snl.no/system/images/8590/k-oslo.gif",
            "heading": "Oslo",
            "license": "fri",
            "paragraph_index": 0,
            "standard_size_url": "http://media.snl.no/system/images/8590/standard_k-oslo.gif",
            "type": "image",
            "xhtml": "<div>\r\n<p>Fylkesv\u00e5pen</p>\r\n</div>"
            },
          ],
          "license_name": "fri",
          "metadata": {
            "area": "454",
            "article_type": "county",
            "author": "670",
            "headword": "Oslo",
            "is_authorized": "1",
            "population": "575 475 (2009)",
            "subject": "1661"
          },
          "metadata_license_name": "fri",
          "subject_title": "Oslo",
          "subject_url": "http://snl.no/.taxonomy/1661",
          "title": "Oslo",
          "url": "http://snl.no/Oslo",
          "xhtml_body": "<div><p>Norges hovedstad</div>\n",
        }
        a = Article.objects.create_article_from_dict('http://snl.no/Oslo', dict_)
        self.assertEquals(a.title, 'Oslo')
