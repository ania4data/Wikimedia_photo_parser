import unittest
from getgloballinks import wiki_photo_parser

class Test_wikiphotoparser(unittest.TestCase):

	def setUp(self):

		self.wiki_photo_parser = wiki_photo_parser()
		self.wiki_photo_parser.read_wiki_address('wiki_image_category_link.txt')
		self.text = self.wiki_photo_parser.read_wiki_address('wiki_image_category_link.txt')
		self.url_counter = 0


	def test_readingfile(self): 
		self.assertEqual(self.text, 'https://commons.wikimedia.org/wiki/Commons:Quality_images/Subject/Microscopic', 'link does not match to Microscopic')

	def test_parsingphoto(self):		
		self.assertEqual(self.wiki_photo_parser.get_photo_address(), 41, 'length of name string should be 41')
		
		self.assertEqual(self.wiki_photo_parser.make_photo_collage(), 100, 'length of index string should be 100')
		
		self.assertEqual(self.wiki_photo_parser.get_photos_infos(), 7, 'length of column of dataframe should be 7')


    
tests = Test_wikiphotoparser()

tests_loaded = unittest.TestLoader().loadTestsFromModule(tests)

unittest.TextTestRunner().run(tests_loaded)