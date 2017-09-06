import os, argparse, sys
from os.path import isfile, join

class FindWord():
	def __init__(self):
		self.dirs = []
		self.word = ''
		self.filename = ''
		self.case_insensitive = False
		self.ext = ''


	def main(self,args):
		self.parse_args(args)
		only_files = []
		
		only_files.extend(self.get_files('', extension=self.ext))
		# Cicle thruogh the directories we find and go through them, getting the files.
		while len(self.dirs):
			d = self.dirs.pop()
			only_files.extend(self.get_files(d, self.ext))

		locations = self.get_locations(only_files)
			
		if len(locations):
			for l in locations:
				print(l)
		else:
			print('Nothing found')
			return None

		return locations


	def parse_args(self,args):
		# Start argparse
		ap = argparse.ArgumentParser('A tool to search for a word or filename in a set of files. It scans the directory it\'s in recursively, which might be resource intensive. A word or filename must be provided, to search for nameless extensions (such as .gitignore) simply use the extension as the filename.')
		ap.add_argument('--ext', metavar="extension", help = 'The extension of the filetype we\'re searching. If not provided it will search ALL files, which will take longer and include binaries that you probably won\'t be able to read. \nIf you only want to search for words in a specific file, put the filename here.', default='')
		ap.add_argument('--w', metavar="word", help='The term to search for.', default='')
		ap.add_argument('--f', metavar="filename", help='A word we want to find in the filename', default='')
		ap.add_argument('--case_insensitive', help='Make the tool not care about the case of the word/file we\'re looking for', default=False, action='store_const', const=True)
		self.ap = ap
		args = ap.parse_args(args)

		# Init variables
		self.word = args.w
		self.filename = args.f
		self.case_insensitive = args.case_insensitive
		self.ext = args.ext

		# Check that a word/filename has been passed
		if(not (self.word or self.filename or self.ext)):
			self.ap.print_help()
			return None


	def get_files(self, path = '', extension=''):
		only_files = []
		if(path):
			files = os.listdir(path)
		else:
			files = os.listdir()

		for f in files:
			if(path):
				f = join(path,f)
			# Checks if it's a file, if not appends to directories
			if isfile(f):
				# If we have an extension we check that the file has said extension, if not we append the file
				if(extension):
					if (extension in str(f)):
						only_files.append(f)
				else:
					only_files.append(f)
			else:
				self.dirs.append(f)

		return only_files


	def get_locations(self, only_files, word='', filename='', case_insensitive=False):
		# in case we want to run this method from the command line and/or test.
		if word:
			self.word = word
		if filename:
			self.filename = filename
		if case_insensitive:
			self.case_insensitive = case_insensitive

		locations = []
		for f in only_files:
			base_loc = str(f)
			if(self.case_insensitive):
				f = f.upper()
				# Take out of method
				self.filename = self.filename.upper()
				self.word = self.word.upper()
			# Check if filename exists and if it's in f
			if(self.filename and self.filename in f):
				locations.append(base_loc)
			# Check if the user queried for a word.
			if self.word:
				x = 0
				with open(f, 'r', encoding='latin-1') as fi:
					for l in fi:
						if(self.case_insensitive):
							l = l.upper()
						# A counter to find the line
						x += 1
						# Check if word exists and if it's in the line.
						if(self.word and self.word in l):
							loc = base_loc+':'+str(x)
							locations.append(loc)
		return locations

if __name__ == '__main__':
	fw = FindWord()
	sys.exit(fw.main(sys.argv[1:]))