# -*- coding: utf-8 -*-

from django.test import TestCase

from texttools import utils

class FindKeyword(TestCase):
    def setUp(self):
        self.fk = utils.KeywordFinder(stopword_fn=None)

    def test_find_keywords_single_simple(self):
        self.assertEqual(self.fk.find_keywords("Fox"),
          ['fox'])

    def test_find_keywords_single_double(self):
        self.assertEqual(self.fk.find_keywords(
              "Fox fox elephant orange fox orange"),
          ['fox', 'orange', 'elephant'])

    def test_find_keywords_single_double_punct(self):
        self.assertEqual(self.fk.find_keywords(
              "Fox. fox elephant. orange fox.orange"),
          ['fox', 'orange', 'elephant'])

    def test_find_keywords(self):
        test_text = ('The fox jumped over the other fox which was cool.'
                     'It really jumped, the fox. Fox it!')
        self.assertEqual(self.fk.find_keywords(test_text),
          ['fox', 'the', 'jumped', 'it', 'over', 'other',
           'which', 'really', 'was', 'cool'])

    def test_find_keywords_with_tags(self):
        self.assertEqual(self.fk.find_keywords(
              "<p>Fox. fox</p> elephant. <div>orange fox.orange"),
          ['fox', 'orange', 'elephant'])

    def test_find_keywords_with_html_entities(self):
        text = 'og&#xA0;st&#xF8;rste by,&#xA0;og '
        self.assertEqual(
            self.fk.find_keywords(text),
            [u'og', u'st\xf8rste', u'by']
        )

    def test_stopword(self):
        self.fk.stopword_set = set(['er', 'eg'])
        self.assertEqual(
            self.fk.find_keywords('Eg er kul'),
            ['kul'])

    def test_stopword_unicode(self):
        self.fk.stopword_set = set([u'øl', 'eg'])
        self.assertEqual(
            self.fk.find_keywords(u'øl eg kul'),
            ['kul'])

    def test_stopword_moar(self):
        self.fk.stopword_set = set(['er', 'eg'])
        self.assertEqual(
            self.fk.find_keywords('Eg er veldig kul og kul og eg og.'),
            ['og', 'kul', 'veldig'])

    def test_find_keywords_with_html_entities_and_stopwords(self):
        text = ('Norges hovedstad og&#xA0;st&#xF8;rste by,&#xA0;og '
                'dessuten&#xA0;en av de eldste byene i landet.')
        self.fk.stopword_set = set(['og', 'en', 'i', 'de', 'av'])
        self.assertEqual(
            self.fk.find_keywords(text),
            [u'landet', u'st\xf8rste', u'norges', u'hovedstad',
             u'dessuten', u'byene', u'eldste', u'by']
        )
