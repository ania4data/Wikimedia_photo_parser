from bs4 import BeautifulSoup
import urllib.request
import re
import json
from PIL import Image
import requests
from io import BytesIO
import numpy as np
from tqdm import tqdm
import pandas as pd
import os



def get_wiki_address(file_name):


	"""Function to read in data from a txt file. The txt file should have
	the wikimedia photo link to quality images e.g.
	https://commons.wikimedia.org/wiki/Commons:Quality_images/Technical/Exposure
            
	Args:
		file_name (string): name of a file to read from
    
	Returns:
		url_list (string): list of wikimedia potential pages to sparse
    
	"""
        
	with open(file_name) as file:
		url_list = []
		line = file.readline()
		while line:
			if('https://commons.wikimedia.org/wiki/' not in line):

				print('-----------Error: link is not from wikimedia common Quality images-------- \n')
				
				break

			url_list.append(line.rstrip())
			line = file.readline()

		file.close()

	return url_list  


def get_photo_address(url_list):

	"""Function to read link to wikimedia url and return address to photo thumbnail,
	address to original size image, address to pages (file) with all info of phtoto and get photo name. 
	e.g. Pond Water Under the Microscope.jpg
	e.g. https://upload.wikimedia.org/wikipedia/commons/9/99/Pond_Water_Under_the_Microscope.jpg
	            
	Args:
		file_name (string): list of wikimedia urls
    
	Returns:
		name_list (string): list of prased photo names
		address_list_thumb (string): list address to thumbnail size photos		
		address_list_original (string): list address to full size size photos
		address_list_original (string): list address to full size size photos
		file_address_list (string) : list of address to complete info link to photo
		url_counter (integer) : a url counter for that counts position from url_list
    """

	url_counter = 0
	html_page = urllib.request.urlopen(url_list[url_counter]) 
	soup = BeautifulSoup(html_page, 'lxml')
	data_name = {}
	name_list = []
	address_list_thumb = []
	address_list_original = []
	file_address_list = []

	count = 0
	for a_ in soup.findAll('a'):
		tmp = a_.get('href')

		if('/wiki/File:' in str(tmp)):
			

			href = tmp


			for link in a_.findAll('img'):

				count += 1

				file_name = (link.get('alt'))
				file_address = (link.get('src'))

				data_name[file_name] = file_address

				name_list.append(file_name.rstrip())
				address_list_thumb.append(file_address.rstrip())
				file_address_tmp = 'https://commons.wikimedia.org/wiki/File:' + file_address.split('/')[-2].rstrip()
				file_address_list.append(file_address_tmp)
				thumb_pix = '/' + file_address.split('/')[-1][0:3]       
				#print(file_address.split(thumb_pix)[0].replace('/thumb',''))
				address_list_original.append(file_address.split(thumb_pix)[0].replace('/thumb',''))


	# json_data1 = json.dumps(data_name)

	# with open('data_name.json', 'w') as outfile1:
	#     json.dump(json_data1, outfile1)

	return name_list, address_list_thumb, address_list_original, file_address_list, url_counter



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def make_photo_collage(address_list_thumb, url_counter):

	"""Function to read link to wikimedia photo urls and make a collage from randomly 100 thumbnail photos,
	the photo_collage.png is then saved under images_(url_counter) path with json file containing photo info index 

	            
	Args:
		address_list_thumb (string): list address to thumbnail size photos
		url_counter (integer) : a url counter for that counts position from url_list
    
	Returns:
		None

    """

	collage_index = {}	

	random_index = list(np.random.choice(range(len(address_list_thumb)), 100))

	new_img = Image.new('RGB', (600,600))
	print('')
	print('Making collage ...')

	for k in tqdm(range(100)):

		collage_index[k] = str(random_index[k])

		image_link = address_list_thumb[random_index[k]]

		response = requests.get(image_link)
		img = Image.open(BytesIO(response.content))

		ratio=img.width/img.height

		if(ratio<1.0):
			new_height=int(60/ratio)
			img_resize=img.resize((60,new_height))
		else:
			new_width=int(60*ratio)
			img_resize=img.resize((new_width,60))

		#img_resize.save('{}.png'.format(k))
		center_y=int(img_resize.width/2.)
		center_x=int(img_resize.height/2.)


		upper = center_y- 30   # PIL  real x,is not actually along width, width->y   height->x
		left = center_x - 30
		lower = center_y + 30
		right = center_x + 30


		img_resize_crop=img_resize.crop((upper,left,lower,right))


		#img_resize_crop.thumbnail((60,60), Image.ANTIALIAS)
		j = int(k/10)
		i = int(k - (j*10))
		#print(k)

		new_img.paste(img_resize_crop, (i*60,j*60))

	directory = 'images_' + str(url_counter)
	if not os.path.exists(directory):
		os.makedirs(directory)

	new_img.save(directory+'/photo_collage.png')
	json_data2 = json.dumps(collage_index)

	with open(directory+'/index_collage.json', 'w') as outfile2:
		json.dump(json_data2, outfile2)


url_list = get_wiki_address('wiki_image_category_link.txt')
name_list, address_list_thumb, address_list_original, file_address_list, url_counter = get_photo_address(url_list)
make_photo_collage(address_list_thumb, url_counter)


#   get author name
#'https://commons.wikimedia.org/wiki/File:Daucus_carota_subsp._maximus_MHNT.BOT.2007.40.407.jpg'   #'https://commons.wikimedia.org/wiki/File:Pond_Water_Under_the_Microscope.jpg'

author_name_list = []
source_list = []
license_link_list = []
license_code_list = []


print('Downloading files ...')

thumbnail = True  #if False download original photo

for counter in tqdm(range(len(file_address_list))):



	html_page = urllib.request.urlopen(file_address_list[counter])

	if(thumbnail == True):

		image_link = address_list_thumb[counter]

	else:

		image_link = address_list_original[counter]

	response = requests.get(image_link)
	img = Image.open(BytesIO(response.content))

	if not os.path.exists('images'):
		os.makedirs('images')

	img.save('images/'+'{}.png'.format(counter))


	soup = BeautifulSoup(html_page, 'lxml')


	count=0
	for img in soup.findAll('tr'):
		text=str(img.get('style'))
		if(((text == "vertical-align: top") or (text == 'valign="top"'))): #and (str(img.get('id') == "fileinfotpl_aut")
			count += 1

			td_list = img.findAll('td')

			for item in td_list:

				if(item.get('id') == "fileinfotpl_src"):

					src_name = str(td_list[1]).strip().split('>')[2][:-6].rstrip()
					if('<' in src_name or (len(src_name) == 0)):
						src_name = None

				if(item.get('id') == "fileinfotpl_aut"):
					auth_name = str(td_list[1]).strip().split('>')[2][:-3].rstrip()
					if('<' in auth_name or (len(auth_name) == 0)):
						auth_name = None

	#print(url_test)
	#print(auth_name)
	#print(src_name)

	author_name_list.append(auth_name)
	source_list.append(src_name)

	for img in soup.findAll('span'):
		text=img.get('class')

		if('licensetpl' in str(text)):


			if('licensetpl_link"' in str(img)):

				license_link = str(img).split('>')[1][:-7].rstrip()
				if('<' in license_link or (len(license_link) == 0)):
					license_link = None				

			if('licensetpl_short' in str(img)):

				license_code = str(img).split('>')[1][:-6].rstrip()
				if('<' in license_code or (len(license_code) == 0)):
					license_code = None

	#print(license_link)
	#print(license_code)

	license_link_list.append(license_link)
	license_code_list.append(license_code)

#print(address_list_original)
#print(file_address_list)
print(len(author_name_list),len(source_list),len(license_link_list),len(license_code_list))	

df = pd.DataFrame([np.array(list(name_list)), np.array(list(author_name_list)),np.array(list(source_list)), np.array(list(license_code_list))\
	              ,np.array(list(license_link_list)),np.array(list(address_list_original)),np.array(list(file_address_list))],\
                  index = ['File_name', 'Author_name', 'Credit', 'license_code', 'license_link', 'link_original_file', 'link_page']).T  
print(df)

df.to_csv('images/photo_fetch_info.csv')

#save photos to disk