
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

class wiki_photo_parser():
	

	def __init__(self):

		self.url_list = []

		self.data_name = {}
		self.name_list = []
		self.address_list_thumb = []
		self.address_list_original = []
		self.file_address_list = []
		self.url_counter = 0

		self.collage_index = {}


		self.author_name_list = []
		self.source_list = []
		self.license_link_list = []
		self.license_code_list = []		


	def read_wiki_address(self, file_name):


		"""Function to read in data from a txt file. The txt file should have
		the wikimedia photo link to quality images e.g.
		https://commons.wikimedia.org/wiki/Commons:Quality_images/Technical/Exposure
	            
		Args:
			file_name (string): name of a file to read from
	    
		Returns:
			url_list (string): list of wikimedia potential pages to sparse
	    
		"""
		print('Getting wiki adresses ...')

		with open(file_name) as file:
			
			line = file.readline()
			while line:
				if('https://commons.wikimedia.org/wiki/' not in line):

					print('-----------Error: link is not from wikimedia common Quality images-------- \n')
					
					break

				self.url_list.append(line.rstrip())
				line = file.readline()

			file.close()

		#return url_list  


	def get_photo_address(self):

		"""Function to read link to wikimedia url and return address to photo thumbnail,
		address to original size image, address to pages (file) with all info of phtoto and get photo name. 
		e.g. Pond Water Under the Microscope.jpg
		e.g. https://upload.wikimedia.org/wikipedia/commons/9/99/Pond_Water_Under_the_Microscope.jpg

		name_list (string): list of prased photo names
		address_list_thumb (string): list address to thumbnail size photos		
		address_list_original (string): list address to full size size photos
		address_list_original (string): list address to full size size photos
		file_address_list (string) : list of address to complete info link to photo
		url_counter (integer) : a url counter for that counts position from url_list
		            
		Args:
			file_name (string): list of wikimedia urls
	    
		Returns:
			length name_list (integer): 

	    """

		print('Getting photo adresses ...')

		
		html_page = urllib.request.urlopen(self.url_list[self.url_counter]) 
		soup = BeautifulSoup(html_page, 'lxml')


		count = 0
		for a_ in soup.findAll('a'):
			tmp = a_.get('href')

			if('/wiki/File:' in str(tmp)):
				

				href = tmp


				for link in a_.findAll('img'):

					
					file_name = (link.get('alt'))
					file_address = (link.get('src'))

					self.data_name[count] = file_address

					self.name_list.append(file_name.rstrip())
					self.address_list_thumb.append(file_address.rstrip())
					file_address_tmp = 'https://commons.wikimedia.org/wiki/File:' + file_address.split('/')[-2].rstrip()
					self.file_address_list.append(file_address_tmp)
					thumb_pix = '/' + file_address.split('/')[-1][0:3]       
					self.address_list_original.append(file_address.split(thumb_pix)[0].replace('/thumb',''))

					count += 1



		directory = 'images_' + str(self.url_counter)
		if not os.path.exists(directory):
			os.makedirs(directory)

		json_data1 = json.dumps(self.data_name)

		with open(directory+'/data_name.json', 'w') as outfile1:
		    json.dump(json_data1, outfile1)

		return len(self.name_list)   


	def make_photo_collage(self):

		"""Function to read link to wikimedia photo urls and make a collage from randomly 100 thumbnail photos,
		the photo_collage.png is then saved under images_(url_counter) path with json file containing photo info index 

		            
		Args:
			address_list_thumb (string): list address to thumbnail size photos
			url_counter (integer) : a url counter for that counts position from url_list
	    
		Returns:

			length of collage index (integer)

	    """


		random_index = list(np.random.choice(range(len(self.address_list_thumb)), 100))

		new_img = Image.new('RGB', (600,600))
		print('')
		print('Making collage ...')

		for k in tqdm(range(100)):

			self.collage_index[k] = str(random_index[k])

			image_link = self.address_list_thumb[random_index[k]]

			response = requests.get(image_link)
			img = Image.open(BytesIO(response.content))

			ratio=img.width/img.height

			if(ratio<1.0):
				new_height=int(60/ratio)
				img_resize=img.resize((60,new_height))
			else:
				new_width=int(60*ratio)
				img_resize=img.resize((new_width,60))

			center_y=int(img_resize.width/2.)
			center_x=int(img_resize.height/2.)


			upper = center_y- 30   # PIL  real x,is not actually along width, width->y   height->x
			left = center_x - 30
			lower = center_y + 30
			right = center_x + 30


			img_resize_crop=img_resize.crop((upper,left,lower,right))

			j = int(k/10)
			i = int(k - (j*10))


			new_img.paste(img_resize_crop, (i*60,j*60))

		directory = 'images_' + str(self.url_counter)
		if not os.path.exists(directory):
			os.makedirs(directory)

		new_img.save(directory+'/photo_collage.png')

		json_data2 = json.dumps(self.collage_index)

		with open(directory+'/index_collage.json', 'w') as outfile2:
			json.dump(json_data2, outfile2)

		return len(self.collage_index)


	def get_photos_infos(self, thumbnail = False, fullsize = False):

		"""Function to read link to wikimedia photo urls and download thumbnail size if fkag is True
		otherwise download original size photos, get the name of auhtor, the credit of the photo, 
		license code, license code link, and makes "photo_fetch_info.csv" with all downloaded photo
		indexed including links, author, credit, license. Also prints few line of csv file in output

		            
		Args:
			name_list (string): list of prased photo names
			address_list_thumb (string): list address to thumbnail size photos		
			address_list_original (string): list address to full size size photos
			address_list_original (string): list address to full size size photos
			file_address_list (string) : list of address to complete info link to photo
			url_counter (integer) : a url counter for that counts position from url_list
	    
		Returns:
			None

	    """


		print('Downloading files ...')

		if(thumbnail == True and thumbnail != fullsize):

			print('. Thumbnail size images .')

		if(fullsize == True and thumbnail != fullsize):

			print('. Original size images .')	


		if(fullsize == True and thumbnail == fullsize):

			print('. Pick one size to download, Only downloading photo infos .')

			
		if(fullsize == False and thumbnail == fullsize):

			print('. Neither photo size selected, Only downloading photo infos .')			


		for counter in tqdm(range(len(self.file_address_list))):


			html_page = urllib.request.urlopen(self.file_address_list[counter])


			if((thumbnail == True and thumbnail != fullsize) or (fullsize == True and thumbnail != fullsize)):


				if(thumbnail == True and thumbnail != fullsize):

					image_link = self.address_list_thumb[counter]

				if(fullsize == True and thumbnail != fullsize):

					image_link = self.address_list_original[counter]


				response = requests.get(image_link)
				img = Image.open(BytesIO(response.content))

				directory = 'images_' + str(self.url_counter)
				if not os.path.exists(directory):
					os.makedirs(directory)

				img.save(directory+'/'+'{}.png'.format(counter))


			soup = BeautifulSoup(html_page, 'lxml')


			count=0
			for img in soup.findAll('tr'):
				text=str(img.get('style'))
				if(((text == "vertical-align: top") or (text == 'valign="top"'))): 
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



			self.author_name_list.append(auth_name)
			self.source_list.append(src_name)

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


			self.license_link_list.append(license_link)
			self.license_code_list.append(license_code)


		df = pd.DataFrame([np.array(list(self.name_list)), np.array(list(self.author_name_list)),np.array(list(self.source_list)), np.array(list(self.license_code_list))\
			              ,np.array(list(self.license_link_list)),np.array(list(self.address_list_original)),np.array(list(self.file_address_list))],\
		                  index = ['File_name', 'Author_name', 'Credit', 'license_code', 'license_link', 'link_original_file', 'link_page']).T  
		print(df.head())

		directory = 'images_' + str(self.url_counter)
		if not os.path.exists(directory):
			os.makedirs(directory)

		df.to_csv(directory+'/photo_fetch_info.csv')

		return df.shape[1]


wiki_parser = wiki_photo_parser()
wiki_parser.read_wiki_address('wiki_image_category_link.txt')
print(wiki_parser.get_photo_address())
print(wiki_parser.make_photo_collage())
print(wiki_parser.get_photos_infos(thumbnail=True))