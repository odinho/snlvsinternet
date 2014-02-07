from django.test import TestCase

from texttools import utils

class FindKeyword(TestCase):
    def test_find_keywords_single_simple(self):
        self.assertEqual(utils.find_keywords("Fox"),
          ['fox'])

    def test_find_keywords_single_double(self):
        self.assertEqual(utils.find_keywords(
              "Fox fox elephant orange fox orange"),
          ['fox', 'orange', 'elephant'])

    def test_find_keywords_single_double_punct(self):
        self.assertEqual(utils.find_keywords(
              "Fox. fox elephant. orange fox.orange"),
          ['fox', 'orange', 'elephant'])

    def test_find_keywords(self):
        test_text = ('The fox jumped over the other fox which was cool.'
                     'It really jumped, the fox. Fox it!')
        self.assertEqual(utils.find_keywords(test_text),
          ['fox', 'the', 'jumped', 'it', 'over', 'other',
           'which', 'really', 'was', 'cool'])

    def test_find_keywords_with_tags(self):
        self.assertEqual(utils.find_keywords(
              "<p>Fox. fox</p> elephant. <div>orange fox.orange"),
          ['fox', 'orange', 'elephant'])


class FindKeywordStopWords(TestCase):
    def test_stopword(self):
        kf = utils.KeywordFinder()
        kf.stopword_set = set(['er', 'eg'])
        self.assertEqual(
            kf.find_keywords('Eg er kul'),
            ['kul'])

    def test_stopword_moar(self):
        kf = utils.KeywordFinder()
        kf.stopword_set = set(['er', 'eg'])
        self.assertEqual(
            kf.find_keywords('Eg er veldig kul og kul og eg og.'),
            ['og', 'kul', 'veldig'])
