import unittest
from find_word import FindWord

class FindWordTestMethod(unittest.TestCase):
	
	def test_get_files(self):
		fw = FindWord()

		files = fw.get_files('test_folder')
		test_files = ['test_folder\\life.py']
		self.assertEqual(files, test_files)

	
	def test_get_locations_word(self):
		fw = FindWord()

		test_locations = [	'test_folder\life.py:15',
							'test_folder\life.py:19',
							'test_folder\life.py:57',
							'test_folder\life.py:59',
							'test_folder\life.py:60',
							'test_folder\life.py:72',
							'test_folder\life.py:76',
							'test_folder\life.py:78',
							'test_folder\life.py:89',
							'test_folder\life.py:95',
							'test_folder\life.py:97']

		locations = fw.get_locations(['test_folder\\life.py'], word='range', filename='', case_insensitive = False)
		self.assertEqual(locations, test_locations)


	def test_get_locations_file(self):
		fw = FindWord()

		locations = ['test_folder\\life.py']
		test_locations = fw.get_locations(['test_folder\\life.py'],  filename='life', case_insensitive=False)
		self.assertEqual(locations, test_locations)

		# TODO: Mock print to test main.
	def test_empty_main(self):
		fw = FindWord()
		self.assertEqual(fw.main(['--w','life']), None)


if __name__ == '__main__':
    unittest.main()