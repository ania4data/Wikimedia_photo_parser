from getgloballinks import wiki_photo_parser



wiki_parser = wiki_photo_parser()
print(wiki_parser)
wiki_parser.read_wiki_address('wiki_image_category_link.txt')
print(wiki_parser.get_photo_address())
print(wiki_parser.make_photo_collage())
print(wiki_parser.get_photos_infos(thumbnail=True))