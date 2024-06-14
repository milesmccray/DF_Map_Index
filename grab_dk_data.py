import requests


def grab_dk_levels():
	"""Grabs all visible levels from dustkid.com/levels.php by cycling through each page."""

	prev = False
	dk_dict = {}

	# Creates a dictionary using data from dustkid.com/levels.php
	while True:
		url = 'https://dustkid.com/levels.php?count=1024&prev='
		if prev:
			dk_level_data = requests.get(url + prev).json()
			prev = dk_level_data['next']
			dk_dict.update(dk_level_data['levels'])
		elif prev is False:
			dk_level_data = requests.get(url).json()
			prev = dk_level_data['next']
			dk_dict = dk_level_data['levels']
		elif prev is None:
			break

	# Swaps level ID to be key rather than filename. NOTE: If dustkid/levels.php has bad data sometimes new levels
	# appear with atlas ID 0. In this case the level will be overwritten by every instance, ending with
	# zettadifficult which is ID 0
	sorted_dk_dict = {}
	for filename in dk_dict:
		level_id = dk_dict[filename].pop('atlas_id')
		dk_dict[filename]['filename'] = filename.replace(' ', '-')  # Makes sure to catch any spaces
		dk_dict_copy = dk_dict.copy()
		sorted_dk_dict[level_id] = dk_dict_copy.pop(filename)

	# Sorts Dictionary by ID
	sorted_dk_dict = dict(sorted(sorted_dk_dict.items(), reverse=True))

	# Builds level URL's and adds to dictionary
	for key in sorted_dk_dict.keys():
		level_leaderboard = f"http://dustkid.com/level/{sorted_dk_dict[key]['filename']}"
		level_url = f"http://atlas.dustforce.com/{key}/{(sorted_dk_dict[key]['filename']).removesuffix(f'-{key}')}"
		level_image = f"http://atlas.dustforce.com/gi/maps/{sorted_dk_dict[key]['filename']}.png"
		sorted_dk_dict[key]['leaderboard'] = level_leaderboard
		sorted_dk_dict[key]['url'] = level_url
		sorted_dk_dict[key]['thumbnail'] = level_image

	return sorted_dk_dict
