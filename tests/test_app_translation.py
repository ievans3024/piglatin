import unittest
from app.piglatin import *

class TranslatorTestCase(unittest.TestCase):

    def test_translatePhrase(self):

        result = translatePhrase('Enter the English text here-that you want translated into Pig Latin. This is accomplished via this HTML document and.')

        expected = 'Enterway ethay Englishway exttay erehay-atthay ouyay antway anslatedtray intoway Igpay Atinlay. Isthay isway accomplishedway iavay isthay HTMLAY ocumentday andway.'

        self.assertEqual(result, expected)

    def test_translateWord(self):
        result = translateWord('egg')
        expected = 'eggway'
        self.assertEqual(result, expected)

        result = translateWord('Quary')
        expected = 'Aryquay'
        self.assertEqual(result, expected)

        result = translateWord('pig')
        expected = 'igpay'
        self.assertEqual(result, expected)

        result = translateWord('Latin')
        expected = 'Atinlay'
        self.assertEqual(result, expected)

        result = translateWord('banana')
        expected = 'ananabay'
        self.assertEqual(result, expected)

        result = translateWord('trash')
        expected = 'ashtray'
        self.assertEqual(result, expected)

        result = translateWord('dopest')
        expected = 'opestday'
        self.assertEqual(result, expected)

        result = translateWord('cheers')
        expected = 'eerschay'
        self.assertEqual(result, expected)
