import json

def load_file(filename):
    with open(filename, "r") as f: #reads the file, translates the json into python objects, returns it to the function
        data = json.load(f)
    return data

def map_weapons_to_areas(weapons, areas):
    data = {}
    for area in areas:
        area_name = area.get('area')
        valid_list = []
        for weapon in weapons:
            if all([weapon.get('stat') in area.get('stats', []), 
                    weapon.get('skill') in area.get('skills', [])]):
                valid_list.append(weapon)
        data[area_name] = {'Valid_Weapons': valid_list}
    matches = {'data': data}
    return matches

def save_matches(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def generate_matches():
    weapons = load_file("weapons.json")
    areas = load_file("areas.json")
    matches = map_weapons_to_areas(weapons['data'], areas['data'])
    matches['version'] = weapons['version']
    save_matches(matches, 'matches.json')