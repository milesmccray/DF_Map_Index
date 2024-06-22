import json
import requests


with open('map_index.json', 'r') as f:
    data = json.load(f)

for level_keys in data.keys():
    if data[level_keys]['status'] == 'published':
        json_data = requests.get(f'https://dustkid.com/json/levelhistory/{data[level_keys]["filename"]}/all').json()
        print(f'Grabbing data from {data[level_keys]["filename"]}')

        ss_count = len(json_data['sses'])  # Grabs the # of SS clears
        if ss_count > 15:
            data[level_keys]['15_SS'] = 'True'
            data[level_keys]['10_SS'] = 'True'
            data[level_keys]['5_SS'] = 'True'
        else:
            data[level_keys]['15_SS'] = 'False'

            if ss_count > 10:
                data[level_keys]['10_SS'] = 'True'
                data[level_keys]['5_SS'] = 'True'
            else:
                data[level_keys]['10_SS'] = 'False'

                if ss_count > 5:
                    data[level_keys]['5_SS'] = 'True'
                else:
                    data[level_keys]['5_SS'] = 'False'


# Re-write data back to JSON file
print('Dumping Data...')
with open('map_index.json', 'w') as f:
    json.dump(data, f, indent=5)
