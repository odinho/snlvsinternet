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
