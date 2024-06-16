import requests
from bs4 import BeautifulSoup
import re


# This file contains some redundant information that is replaced down the line, but can be used just to grab a json file
# of all published maps on atlas instead

def grab_atlas_levels():
	"""Creates a dictionary containing all published levels on atlas using HTML scraping"""
	num = 0
	atlas_levels = {}

	# Regex
	level_regex = '\/(\d*)\/(.*)">(.*)<\/a>'
	level_thumbnail_regex = "'(.*)'"
	level_author_regex = '">(.*)<\/a>'

	while True:
		page = requests.get(f'https://atlas.dustforce.com/?start={num}')
		soup = BeautifulSoup(page.content, "html.parser")
		atlas_html = soup.find_all('div', {'class': 'map map-page-list paper'})

		if atlas_html:  # Checks to make sure atlas_html is not empty (end of list)
			for map_html in atlas_html:
				# Grab Level Information From HTML
				level_html = map_html.find('a', {'class': 'dark-link'})
				level_id, level_url_name, level_name = re.search(level_regex, str(level_html)).group(1, 2, 3)

				# Grab Level Thumbnail From HTML
				level_thumbnail_html = map_html.find('div', {'class': 'map-image'})
				level_thumbnail = re.search(level_thumbnail_regex, str(level_thumbnail_html)).group(1)

				# Grab Author From HTML
				level_author_html = map_html.find('strong')
				level_author = re.search(level_author_regex, str(level_author_html)).group(1)

				# Creates Leaderboard/Atlas Link
				level_leaderboard = f'http://dustkid.com/level/{level_url_name}-{level_id}'
				level_url = f'http://atlas.dustforce.com/{level_id}/{level_url_name}'
				level_filename = f'{level_name}-{level_id}'.replace(' ', '-')

				# Combine into Dictionary
				atlas_levels[int(level_id)] = {'name': level_name, 'filename': level_filename, 'author': level_author,
											   'status': 'published', 'level_type': 'N/A', 'leaderboard': level_leaderboard,
											   'url': level_url, 'thumbnail': level_thumbnail}

			print(f'Loading page: https://atlas.dustforce.com/?start={num}')
			num += 10  # Increases the count in the atlas URL by 10 maps to get to next page

		else:
			print('Adding hidden/unpublished levels...')
			break

	all_levels = add_hidden_levels(atlas_levels)
	return all_levels


def add_hidden_levels(atlas_dict):
	"""Adds hidden levels to existing dictionary"""
	all_levels = atlas_dict.copy()
	level_id_prev = None
	first_id = True

	# Loop over each key to see if previous key exists, Add to all_levels dictionary
	for level_id in atlas_dict.keys():
		if first_id:
			level_id_prev = level_id
			first_id = False
		else:
			if int(level_id_prev) - 1 == int(level_id):
				level_id_prev = level_id
				continue
			else:
				#  Adds ID's for every ID between previous and current ID
				for hidden_id in range(int(level_id_prev)-1, int(level_id), -1):
					all_levels[hidden_id] = {'level': 'N/A', 'filename': 'N/A', 'author': 'N/A', 'status':
						'hidden/unpublished', 'leaderboard': 'N/A', 'url': 'N/A', 'thumbnail': 'N/A'}
					level_id_prev = level_id  # Moves the previous ID down 1 to compensate for hidden map

	# Add last hidden levels to the dictionary (Stops at ID 93, the rest are Hitbox testing levels)
	last_id = list(atlas_dict.keys())[-1]
	for hidden_id in range((int(last_id) - 1), 92, -1):
		all_levels[hidden_id] = {'level': 'N/A', 'filename': 'N/A', 'author': 'N/A', 'status':
			'hidden/unpublished', 'leaderboard': 'N/A', 'url': 'N/A', 'thumbnail': 'N/A'}

	# Sorts Levels back into ID order
	all_levels = dict(sorted(all_levels.items(), reverse=True))

	return all_levels





