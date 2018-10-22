import unittest
from getgloballinks import wiki_photo_parser

class Test_wikiphotoparser(unittest.TestCase):

    def setUp(self):

        self.wiki_photo_parser = wiki_photo_parser()
        self.link_list = list('https://commons.wikimedia.org/wiki/Commons:Quality_images/Subject/Microscopic')
        self.url_counter = 0

    def test_functions(self): 


        self.assertEqual(elf.wiki_photo_parser.get_photo_address(self.link_list), 41, 'length of name string should be 41')
        self.assertEqual(elf.wiki_photo_parser.make_photo_collage(), 41, 'length of index string should be 41')
        self.assertEqual(elf.wiki_photo_parser.get_photos_infos(), 7, 'length of column of dataframe should be 7')


    
tests = Test_wikiphotoparser()

tests_loaded = unittest.TestLoader().loadTestsFromModule(tests)

unittest.TextTestRunner().run(tests_loaded)