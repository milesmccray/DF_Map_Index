import json


# (Level_type: 0:Normal, 21Nexus, 2:Nexus MP, 3:KotH, 4:Survival, 5:Boss, 6:Dustmod)
def create_map_index(all_levels, dk_level_data):
	"""Creates a new dictionary using information from both existing dictionaries"""

	# Remove last entry of dk_level_data (zettadifficult error map))
	del dk_level_data[0]

	map_index = {}
	id_list = list(key for key in all_levels.keys())
	for level_id in id_list:
		if level_id in dk_level_data.keys():
			map_index[level_id] = ({
				'name': dk_level_data[level_id]['name'], 'filename': dk_level_data[level_id]['filename'],
				'author': dk_level_data[level_id]['author'], 'status': all_levels[level_id]['status'],
				'leveltype': dk_level_data[level_id]['level_type'], 'leaderboard': dk_level_data[level_id]['leaderboard'],
				'url': dk_level_data[level_id]['url'], 'thumbnail': dk_level_data[level_id]['thumbnail']})

		else:  # Incase dk_data is missing newest maps, default to atlas information
			map_index[level_id] = all_levels[level_id]

	# Create JSON
	with open('map_index.json', 'w') as f:
		json.dump(map_index, f, indent=5)
