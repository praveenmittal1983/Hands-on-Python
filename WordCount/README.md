Program to find word occurrences
================================

Using this program, we can the find occurrences of all the words in a given file. The most frequent word will be listed at the top.

Arguments
---------

```
--filepath FILEPATH         Input filename that contains the data. It is a mandatory argument.
```

Usage
------

To run the program:

```
python .\run.py -f .\data\samplefile.txt
```

To run the test cases:

```
python -m unittest -v .\tests\test_wordcount.py
```

Installation Steps
-----------------

1. Install Python

```
https://wiki.python.org/moin/BeginnersGuide/Download
```

2. The following (non-default) packages are needed to run the unit tests:

```
pip3 install parameterized; 
pip3 install mock
```