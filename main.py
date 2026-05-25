import json
import itertools

def load_file(filename):
    with open(filename, "r") as f: #reads the file, translates the json into python objects, returns it to the function
        data = json.load(f)
    return data

def format_weapons(weapons):
    lines = [f"{i}. {weapon.get('name')}" for i, weapon in enumerate(weapons, 1)]
    return "\n".join(lines)

def translate_user_weapon_input(number_string, weapons):
    user_numbers = number_string.split(',')
    w_list = []
    for number in user_numbers:
        weapon = int(number.strip())
        w_list.append(weapons[(weapon-1)])
    return w_list

def find_areas(target_weapons, areas):
    matches = []
    for area in areas:
        match = {'Area_Name': area.get('area'), 'Valid_Weapons': []}
        for weapon in target_weapons:
            if all([weapon.get('stat') in area.get('stats'), weapon.get('skill') in area.get('skills')]):
                match['Valid_Weapons'].append(weapon)
        matches.append(match)
    sorted_matches = sorted(matches, key=lambda x: len(x['Valid_Weapons']), reverse=True)
    return sorted_matches

def find_optimal_settings(matches, areas):
    area_map = {a.get('area'): a for a in areas}
    for match in matches:
        name = match['Area Name']
        data = area_map[name]

def main():
    weapons = load_file("weapons.json") #calls the function to grab the weapons list from the .json and convert it to a python list of dictionaries
    areas = load_file("areas.json")
    print(format_weapons(weapons))
    target_weapons = translate_user_weapon_input(input(f"Please input which weapon numbers you want to focus on, separated by commas.\nEX: '1, 5, 32' will request focus on {weapons[0]['name']}, {weapons[4]['name']}, and {weapons[31]['name']}: "), weapons)
    matches = find_areas(target_weapons, areas)
    print(matches)
main()