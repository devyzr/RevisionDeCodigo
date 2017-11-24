# WordFinder
A simple python script to help with manual code review.

## Dependencies
Written in Python 3, it only depends on os, argparse and sys, so no need to import anything.

## Using it

Here's the help output:

```
usage: A tool to search for a word or filename in a set of files. It scans the
       directory it's in recursively, which might be resource intensive. A word
       or filename must be provided, to search for nameless extensions (such as
       .gitignore) simply use --ext to search.
       
       [-h] [--w word] [--f filename] [--ext extension] [--case_insensitive]
       [--dir DIR] [--ignore IGNORE]

optional arguments:
  -h, --help          show this help message and exit
  --w word            The word to search for.
  --f filename        A word we want to find in the filename.
  --ext extension     The extension of the filetype we're searching. If not
                      provided it will search ALL files, which will take
                      longer and include binaries that you probably won't be
                      able to read. If you only want to search for words in a
                      specific file, put the filename here.
  --case_insensitive  Make the tool not care about the case of the word/file
                      we're looking for.
  --dir DIR           Search in the specified directory.
  --ignore IGNORE     A string we want to ignore in the filename, we can
                      ignore many strings if we separatethem with commas.
```
