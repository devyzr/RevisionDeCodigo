import os
import argparse
import sys
import re
import json

from os.path import isfile, join


class FindWord:
    def __init__(self):
        self.dirs = []
        self.word = ""
        self.filename = ""
        self.case_insensitive = False
        self.ext = ""

    def main(self, args):
        self.parse_args(args)
        only_files = []

        only_files.extend(self.get_files(self.dir, extension=self.ext))
        # Cicle through and traverse dirs
        while len(self.dirs):
            current_dir = self.dirs.pop()
            only_files.extend(self.get_files(current_dir, self.ext))

        locations = self.get_locations(only_files)

        if len(locations):
            if self.print_lines:
                pass
            else:
                for l in locations:
                    print(l)
        else:
            print("Nothing found")
            return None

    # Parses CLI arguments
    def parse_args(self, args):
        argparse_text = (
            "A tool to search for a word or filename in a set of "
            "files. It scans the directory it's in recursively, "
            "which might be resource intensive. A word, filename,"
            " regex or regex preset must be provided."
        )
        ap = argparse.ArgumentParser(argparse_text)
        ap.add_argument(
            "--w", metavar="WORD", help="The word to search for.", default=""
        )
        ap.add_argument(
            "--f",
            metavar="FILENAME",
            help="A word we want to find in the filename.",
            default="",
        )
        # ToDo: Add filename regex.
        ap.add_argument(
            "--regex",
            help="A regex to search for inside a file. "
            "Remember that the script searches line by line, "
            "meaning multi-line regexes won't work.",
            default="",
            metavar="REGULAR_EXPRESSION",
        )
        ap.add_argument(
            "--regex_preset",
            help="A series of regex presets, "
            "currently has internal support for 'java_sql',"
            "additional presets can be loaded from the 'presets"
            ".json' file. You can add presets as well. You can"
            "see the available presets by using 'print_presets'"
            " as the preset name.",
            metavar="PRESET_NAME",
        )
        ap.add_argument(
            "--ext",
            metavar="EXTENSION",
            help="The extension "
            "of the filetype we're searching. If not provided it "
            "will search ALL files, which will take longer and "
            "include binaries that you probably won't be able to "
            "read. \nIf you only want to search for words in a "
            "specific file, put the filename here.",
            default="",
        )
        ap.add_argument(
            "--case_insensitive",
            help="Make the tool not care "
            "about the case of the word/file we're looking for.",
            default=False,
            action="store_const",
            const=True,
        )
        ap.add_argument(
            "--dir",
            help="Search in the specified directory.",
            default="",
            metavar="PATH_NAME",
        )
        ap.add_argument(
            "--ignore",
            help="A string we want to ignore in the "
            "filename, we can ignore many strings if we separate "
            "them with commas.",
            default="",
            metavar="IGNORE_STRING",
        )
        ap.add_argument(
            "--print_lines",
            help="Print the line that coincides " "with the search term.",
            default=False,
            action="store_const",
            const=True,
        )

        self.ap = ap
        args = ap.parse_args(args)

        # Init argparse variables
        self.word = args.w
        self.filename = args.f
        self.case_insensitive = args.case_insensitive
        self.ext = args.ext
        self.dir = args.dir
        self.print_lines = args.print_lines

        if args.regex_preset:
            self.regex = self.get_preset(args.regex_preset)
        elif args.regex:
            self.regex = re.compile(args.regex)
        else:
            self.regex = False

        if args.ignore:
            self.ignore = args.ignore.split(",")
        else:
            self.ignore = [""]

        # Check that a search term has been passed, if not print help and exit
        if not (self.word or self.filename or self.regex):
            self.ap.print_help()
            return None

    # Gets the files of a directory, if no directory is passed gets root dir
    def get_files(self, path="", extension=""):
        only_files = []
        if path:
            files = os.listdir(path)
        else:
            files = os.listdir()

        for f in files:
            if path:
                f = join(path, f)
            # Checks if it's a file, if not appends to directories
            if isfile(f):
                str_f = str(f)
                # Check for extension if specified, if not we append the file
                if extension:
                    ext_len = len(extension)
                    if extension == str_f[-ext_len:]:
                        only_files.append(f)
                else:
                    only_files.append(f)
            else:
                self.dirs.append(f)

        return only_files

    # Search the files we have for filenames or words in the files
    def get_locations(self, only_files, word="", filename="", case_insensitive=False):
        # These if statements are used for tests and CLI use of method
        if word:
            self.word = word
        if filename:
            self.filename = filename
        if case_insensitive:
            self.case_insensitive = case_insensitive

        # file is the whole filename including directory
        locations = []
        for file in only_files:
            # duplicate file in case we need to uppercase word,
            # this avoids errors when opening file later on.
            comp_file = str(file)
            if self.ignore != [""]:
                if any(bad_ext == file[-len(bad_ext) :] for bad_ext in self.ignore):
                    continue
            base_loc = str(file)
            if self.case_insensitive:
                comp_file = file.upper()
                # Take out of method
                self.filename = self.filename.upper()
                self.word = self.word.upper()
            # Check if filename exists and if it's in file
            if self.filename and self.filename in comp_file:
                # Split to only search filename.
                file_parts = comp_file.split(os.sep)
                if self.filename in file_parts[-1]:
                    locations.append(base_loc)

            # Check if user needs to find words in a specific file.
            if self.word and self.filename:
                if base_loc not in locations:
                    continue
            x = 0
            with open(file, "r", encoding="latin-1") as o_file:
                self.prev_line = 0
                for line in o_file:
                    unmodded_line = line
                    if self.case_insensitive:
                        line = line.upper()
                    # A counter to find the line
                    x += 1
                    # Check if word exists and if it's in the line.
                    if self.word and self.word in line:
                        if base_loc in locations:
                            locations.remove(base_loc)
                        loc = base_loc + ":" + str(x)
                        locations.append(loc)
                        if self.print_lines:
                            self.print_results(loc, unmodded_line, x)

                    # Check for regex matches
                    if self.regex:
                        if self.regex.search(line):
                            loc = base_loc + ":" + str(x)
                            locations.append(loc)
                            if self.print_lines:
                                self.print_results(loc, unmodded_line, x)
                if self.filename and self.word and base_loc in locations:
                    locations.remove(base_loc)

        return locations

    # A method to avoid rewriting code that lets us print
    # the lines of results we find.
    def print_results(self, l_location, l_content, current_l):
        text = l_content.strip()
        text = text.encode(sys.stdout.encoding, errors="replace")
        line_difference = current_l - self.prev_line
        if self.prev_line != 0 and line_difference == 1:
            print(text)
        else:
            print("\n%s" % l_location)
            print(text)
        self.prev_line = current_l

    def get_preset(self, preset_option):
        # A dict of presets that are commonly used, to avoid having to copy
        # presets.json
        # SQL words, separated for use in other langs.
        sql_words = (
            "(select|SELECT|insert|INSERT|where|WHERE|delete|DELETE|"
            "update|UPDATE|from|FROM|join|JOIN|like|LIKE|upper\s*\(|"
            "UPPER\s*\(|order\ by|ORDER\ BY|case|CASE|when|WHEN|then|"
            "THEN|else|ELSE|ltrim|LTRIM|rtrim|RTRIM|and|AND|SYSDATE|"
            "sysdate|VALUES|values|SMALLINT|smallint|VARCHAR|varchar"
            "DECLARE|declare|DATETIME|datetime|MONEY|money)"
        )
        preset_dict = {
            "java_sql": '".*' + sql_words + '.*"',
            # High priority danger words for Python
            "danger_noodle": "(subprocess|system|popen|exec|eval|"
            "pickle|shelve|yaml|sqlite3|pypyodbc|jsonpickle|urlib2|"
            "socket|fork|kill|execfile|__import__|path|spawn|popen2"
            "|commands|input|get|post|(commands\.)*getoutput|"
            "(commands\.)*getoutput|(commands\.)*getstatus|"
            "(commands\.)*getstatusouput|compile|(cPickle\.)*load|"
            "(cPickle\.)*loads|(marshal\.)*load|(marshal\.)*loads|"
            "(os\.)*execl|(os\.)*execle|(os\.)*execlp|"
            "(os\.)*execlpe|(os\.)*execv|(os\.)*execve|"
            "(os\.)*execvp|(os\.)*execvpe|(os\.)*popen|"
            "(os\.)*popen2|(os\.)*popen3|(os\.)*popen4|"
            "(os\.)*spawnl|(os\.)*spawnle|(os\.)*spawnlp|"
            "(os\.)*spawnlpe|(os\.)*spawnv|(os\.)*spawnve|"
            "(os\.)*spawnvp|(os\.)*spawnvpe|(os\.)*startfile"
            "|(os\.)*system|(pickle\.)*load|(pickle\.)*loads|"
            "(popen2\.)*popen2|(popen2\.)*popen3|(popen2\.)*popen4|"
            "shelve\.open|(subprocess\.)*call|"
            "(subprocess\.)*check_call|(subprocess\.)*check_output|"
            "(subprocess\.)*Popen|(yaml\.)*load|requests)",
            # Low priority danger words for Python
            "not_so_danger_noodle": "(logging|print|open|tarfile|"
            "zipfile|file|getattr|setattr|delattr)",
        }

        preset_json = {}
        json_filename = "presets.json"
        if os.path.isfile(json_filename) and os.stat(json_filename).st_size != 0:
            with open(json_filename, "r") as json_file:
                preset_json = json.load(json_file)
            preset_dict = {**preset_dict, **preset_json}

        if preset_option == "print_presets":
            print("Available presets are:")
            for preset in preset_dict:
                print(">>> %s" % preset)
                print(preset_dict[preset])
                print()
            sys.exit()

        if preset_option not in preset_dict:
            print("Coulnd't find '%s', available presets are:" % preset_option)
            for preset in preset_dict:
                print(">>> %s" % preset)
                print(preset_dict[preset])
                print()
            sys.exit()
        else:
            raw_regex = preset_dict[preset_option]
            regex = re.compile(raw_regex)
        return regex


if __name__ == "__main__":
    fw = FindWord()
    sys.exit(fw.main(sys.argv[1:]))
