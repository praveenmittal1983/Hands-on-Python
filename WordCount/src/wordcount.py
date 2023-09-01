import os
from collections import Counter

class WordCount:
    def __init__(self, file_path):
        self.file_path = file_path
        self.word = []

    # Validating input file
    def validate_filepath(self):
        if os.path.isfile(self.file_path):
            return True

    # Count the occurunces of the word in a given file
    def word_count(self):
        try:
            with open(self.file_path, 'r') as f:
                data = f.read().replace('\n', ' ').lower()  # Combine all the lines from file into a large single line
                self.words = Counter(data.split(' ')).most_common() # Finding occurrences of each word with most frequent word on the top
                self.words = sorted(sorted(self.words, key=lambda x:(x[1], x[0])), key=lambda x:(x[1]), reverse=True) # Ordering the words retaining the most frequent word on the top
                return self.words
        except FileNotFoundError:
            raise

    # Print one word per line
    def print_results(self):
        for k,v in self.words:
            print(f'{k}: {v}')