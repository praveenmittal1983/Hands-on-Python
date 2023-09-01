import unittest, mock
from parameterized import parameterized
from src.wordcount import WordCount

class WordCountTestCase(unittest.TestCase):
    
    # Word Count
    def test_word_count_happy_path(self):
        read_data = "Hello Test Test"
        mock_open = mock.mock_open(read_data=read_data)
        with mock.patch("builtins.open", mock_open):
            wc = WordCount('some_filename')
            result = wc.word_count()
            self.assertEqual(result, [('test',2),('hello',1)])

    def test_word_count_fail_path(self):
        with self.assertRaises(FileNotFoundError):
            wc = WordCount('some_filename')
            wc.word_count()

    # Validate FilePath
    @parameterized.expand(['.\data\samplefile.txt'])
    def test_validate_filepath_happy_path(self, value):
        wc = WordCount(value)
        result = wc.validate_filepath()
        self.assertEqual(result, True)

    @parameterized.expand(['abcfilepath', './34'])
    def test_validate_filepath_with_invalid_path(self, value):
        wc = WordCount(value)
        result = wc.validate_filepath()
        self.assertEqual(result, None)