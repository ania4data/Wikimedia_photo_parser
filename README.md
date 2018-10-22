# Wikimedia-common photo parsing package

- In this package Wikimedia common quality images are parsed to first download the photo link.
- The photos links are used to download photos either original size or thumbnail size
- From 100 random images from the main link a photo grid/collage is created
- All related info with regard to photos (e.g. photo name, author name, credit, license, links) all saved in an output `photo_fetch_info.csv file`

<p align="center"> 
<img src="https://github.com/ania4data/Wikimedia_photo_parser/blob/master/wikiphotoparser/samples/photo_collage_sunset.png">
</p>
![sunset](/wikiphotoparser/samples/photo_collage_sunset.png)


## Dependecies and packages:

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



## General repository content:

- A pyhon file: `getgloballinks.py`
- Image folder (`samples`):
	- containing photos in the notebook
	- a collage photo `photo_collage.png`
	- a `photo_fetch_info.csv` containing all links/author and photo index
	- two json files: for index to photo adress `data_name.json`, and index to index of collage `index_collage.json`

- A `txt` file: `wiki_image_category_link.txt` contain link to wikimedia common the to be sparsed
- Two example file `*.py`: `example.py` and `example_with_pip_install`
- A package requirement file:  `requirements.txt`
- MIT License file


## Basic Usage for command line

- Clone the repository use: `git clone https://github.com/ania4data/Wikimedia_photo_parser.git`
- Create a virtual enviroment where `requirements.txt` is located: 
```
conda update python
python3 -m venv name_of_your_choosing
source name_of_your_choosing/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## How to run the code without pip install

Follow `example.py` in the  wikiphotoparser folder

## How to run the code with pip install

In your virtual enviroment `name_of_your_choosing` where `setup.py` located do the following:

`pip install .`

then follow `example_with_pip_install` (located in wikiphotoparser folder) in your python enviroment


## To download photos with their info in csv

- default: thumbnail `False`/fullsize `False` get photo info (the same for both `True`)
- thumbnail `True` downloads thumbnail size only
- fullsize `True` downloads original size only
- the output will bge saved to `/images_0` folder

wiki_parser.get_photos_infos(thumbnail=True)


## Source dataset

Data is input link to a wikimedia page e.g. 

- https://commons.wikimedia.org/wiki/Commons:Quality_images/Subject/Microscopic
- https://commons.wikimedia.org/wiki/Commons:Quality_images/Technical/Exposure
- https://commons.wikimedia.org/wiki/Commons:Quality_images/Subject/Astronomy
- https://commons.wikimedia.org/wiki/Commons:Quality_images/Subject/Fungi
- https://commons.wikimedia.org/wiki/Commons:Quality_images/Subject/Sunsets
