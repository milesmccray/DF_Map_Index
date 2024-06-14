import grab_id_list
import grab_dk_data
import combine_map_index

if __name__ == '__main__':
	all_levels = grab_id_list.grab_atlas_levels()
	#with open('map_index.json', 'r') as f:
	#all_levels = json.load(f)
	#all_levels = {int(key):value for key, value in all_levels.items()}
	dk_level_data = grab_dk_data.grab_dk_levels()
	combine_map_index.create_map_index(all_levels, dk_level_data)
