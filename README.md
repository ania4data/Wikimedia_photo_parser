# A package to parse Wikimedia common pages to download photographs and related infos and make a collage

- In this package Wikimedia common quality images are parsed to first download the photo link.
- The photos links are used to download photos either original size or thumbnail size
- From 100 random images from the main link a photo grid/collage is created
- All related info with regard to photos (e.g. photo name, author name, credit, license, links) all saved in an output `photo_fetch_info.csv file`

<p align="center"> 
<img src="https://github.com/ania4data/Wikimedia_photo_parser/blob/master/wikiphotoparser/samples/photo_collage_sunset.png">
</p>
![sunset](/wikiphotoparser/samples/photo_collage_sunset.png)


# Dependecies and packages:

- Python 3.x
- numpy
- pandas
- BeautifulSoup
- urllib (request)
- re
- json
- PIL
- requests
- io
- tqdm
- os



# Repository content:

- A pyhon file: `getgloballinks.py`
- Image folder (`samples`):
	- containing photos in the notebook
	- a collage photo `photo_collage.png`
	- a `photo_fetch_info.csv` containing all links/author and photo index
	- two json files: for index to photo adress `data_name.json`, and index to index of collage `index_collage.json`

- A `txt` file: `wiki_image_category_link.txt` contain link to wikimedia common the to be sparsed
- MIT License file


# Basic Usage for command line

- Clone the repository use: `git clone https://github.com/ania4data/Wikimedia_photo_parser.git`

# How to run 

## To initilize

wiki_parser = wiki_photo_parser()

## To read wikimedia link from file

wiki_parser.read_wiki_address('wiki_image_category_link.txt')

## To get photo addresses

wiki_parser.get_photo_address()

## To get photo collage

wiki_parser.make_photo_collage()

## To download photos with their info in csv

- default: thumbnail `False`/fullsize `False` get photo info (the same for both `True`)
- thumbnail `True` downloads thumbnail size only
- fullsize `True` downloads original size only
- the output will bge saved to `/images_0` folder

wiki_parser.get_photos_infos(thumbnail=True)


# Source dataset

Data is input link to a wikimedia page e.g. (https://commons.wikimedia.org/wiki/Commons:Quality_images/Subject/Microscopic)
