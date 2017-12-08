# WordFinder
A simple Python 3 script to help with manual code review, designed so we can just copy/paste it to wherever we need to search in the system.

## Dependencies
Written in Python 3, it only depends on **os**, **argparse**, **json** and **sys**, so no need to import or ```pip install``` anything. 

## Using it

Here's the help output:

```
usage: A tool to search for a word or filename in a set of files. It scans the
       directory it's in recursively, which might be resource intensive.
       A word, filename, regex or regex preset must be provided.
       
       [-h] [--w WORD] [--f FILENAME] [--regex REGULAR_EXPRESSION]
       [--reg_preset PRESET_NAME] [--ext EXTENSION] [--case_insensitive]
       [--dir PATH_NAME] [--ignore IGNORE_STRING] [--print_lines]

optional arguments:
  -h, --help            show this help message and exit
  --w WORD              The word to search for.
  --f FILENAME          A word we want to find in the filename.
  --regex REGULAR_EXPRESSION
                        A regex to search for inside a file
  --reg_preset PRESET_NAME
                        A series of regex presets, currently has internal
                        support for 'java_sql',additional presets can be
                        loaded from the 'presets.json' file. You can add
                        presets as well.
  --ext EXTENSION       The extension of the filetype we're searching. If not
                        provided it will search ALL files, which will take
                        longer and include binaries that you probably won't be
                        able to read. If you only want to search for words in
                        a specific file, put the filename here.
  --case_insensitive    Make the tool not care about the case of the word/file
                        we're looking for.
  --dir PATH_NAME       Search in the specified directory.
  --ignore IGNORE_STRING
                        A string we want to ignore in the filename, we can
                        ignore many strings if we separate them with commas.
  --print_lines         Print the line that coincides with the search term.
```

#### Notes:
Searching for words, filenames, regexes or regex presets is mutually exclusive. We can include a regex preset instead of a regex.

If we only want to search inside a filename with a specific name we can use the '--ext' argument, since it only checks that the string provided is in the filename, which might not as strict as desireable, but gives us some flexibility.

'--ignore' only works on filenames.


### Regex Presets

Presets can be useful in case we repeatedly need to use a regex or it's not possible for us to input it via the command line due to special symbols. Simply add the presets filename and the regex in JSON notation into the 'presets.json' file. The file doesn't need to be present, this allows us to copy/paste the script to wherever we need to use it.


Remember to double escape your backslashes unless they're escaping double quotes. Here we escape spaces:

```
{
    "example":"\"(\\ a\\ |b|\\ c\\ )\""
}
```

The 'presets.json' file doesn't need to be present to use the standalone script.