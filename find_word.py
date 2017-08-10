import os, argparse, sys
from os.path import isfile, join

class FindWord():
	def __init__(self):
		# Start argparse
		ap = argparse.ArgumentParser('A tool to search for a word or filename in a set of files. It scans the directory it\'s in recursively, which might be resource intensive. A word or filename must be provided, to search for nameless extensions (such as .gitignore) simply use the extension as the filename.')
		ap.add_argument('--extension', help = 'The extension of the filetype we\'re searching. If not provided it will search ALL files, which will take longer.', default='')
		ap.add_argument('--w', help='The term to search for.', default='')
		ap.add_argument('--f', help='A word we want to find', default='')
		ap.add_argument('--case_insensitive', help='Make the tool not care about the case of the word/file wer\'re looking for', default=False, action='store_const', const=True)
		args = ap.parse_args()

		# Init variables
		self.only_files = []
		self.dirs = []
		self.locations = []
		self.word = args.w
		self.filename = args.f
		self.case_insensitive = args.case_insensitive
		self.ext = args.extension

		# Check that a word/filename has been passed
		if(not (self.word or self.filename or self.ext)):
			ap.print_help()
			sys.exit()


	def main(self):
		self.get_files('', self.ext)
		# Cicle thruogh the directories we find and go through them, getting the files.
		while len(self.dirs):
			d = self.dirs.pop()
			self.get_files(d, self.ext)

		self.get_locations()
			
		if len(self.locations):
			for l in self.locations:
				print(l)
		else:
			print('Nothing found')


	def get_files(self, path = '', extension=''):
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
						self.only_files.append(f)
				else:
					self.only_files.append(f)
			else:
				self.dirs.append(f)


	def get_locations(self):
		for f in self.only_files:
			base_loc = str(f)
			if(self.case_insensitive):
				f = f.upper()
				self.filename = self.filename.upper()
				self.word = self.word.upper()
			# Check if filename exists and if it's in f
			if(self.filename and self.filename in f):
				self.locations.append(base_loc)
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
							self.locations.append(loc)

if __name__ == '__main__':
	fw = FindWord()
	fw.main()