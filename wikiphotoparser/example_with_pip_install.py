import wikiphotoparser



wiki_parser = wikiphotoparser.wiki_photo_parser()
print(wiki_parser)
wiki_parser.read_wiki_address('wikiphotoparser/wiki_image_category_link.txt')
print(wiki_parser.get_photo_address())
print(wiki_parser.make_photo_collage())
print(wiki_parser.get_photos_infos(thumbnail=True))