import sys
import os
import json
from itertools import combinations
from generate_matches import generate_matches

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
        w_list.append(weapons['data'][(weapon-1)])
    return w_list

def find_optimal_settings(matches, target_weapons):
    all_cases = {}
    for area in matches['data'].keys():
        area_weapons = matches['data'][area]['Valid_Weapons']
        target_attributes = []
        target_skills = []
        target_stats = []
        for weapon in target_weapons:
            if weapon in area_weapons:
                if weapon.get('attribute') not in target_attributes: target_attributes.append(weapon.get('attribute'))
                if weapon.get('skill') not in target_skills: target_skills.append(weapon.get('skill'))
                if weapon.get('stat') not in target_stats: target_stats.append(weapon.get('stat'))
        while len(target_attributes) < 3:
            target_attributes.append('free')
        for combo in combinations(target_attributes, 3):
            for lock_type, lock_options in [('skill', target_skills), ('stat', target_stats)]:
                for lock_name in lock_options:
                    count = 0
                    matching_weapon_list = []
                    case_key = f"{area} | {combo} | {lock_type.upper()}: {lock_name}"
                    
                    for weapon in target_weapons:
                        if weapon in area_weapons:
                            if weapon.get('attribute') in combo and weapon.get(lock_type) == lock_name:
                                count += 1
                                matching_weapon_list.append(weapon['name'])
                    
                    if count > 0:
                        all_cases[case_key] = {
                            'count': count, 
                            'matching_weapons': matching_weapon_list
                        }
    return all_cases

def format_solution(all_cases, target_weapons):
    remaining_names = [w['name'] for w in target_weapons]
    output_string = "Endministrator, here are the results. For optimal essence farming, go to the following areas with the given settings to get the listed weapon's essences."
    while remaining_names:
        best_case_key = None
        best_weapon_list = []
        max_count = 0
        for case_key, case_data in all_cases.items():
            current_matches = [w for w in case_data['matching_weapons'] if w in remaining_names]
            current_count = len(current_matches)
            if current_count > max_count:
                max_count = current_count
                best_case_key = case_key
                best_weapon_list = current_matches
        if not best_case_key:
            break
        output_string += f"\n{best_case_key} | for -> {', '.join(best_weapon_list)}"
        for w in best_weapon_list:
            remaining_names.remove(w)
    return output_string


def main():
    if not os.path.exists("weapons.json") or not os.path.exists("areas.json"):
        sys.exit("Critical Error: Core data files (weapons/areas) are missing! Endministrator, please update the program via Github!")
    weapons = load_file("weapons.json") #calls the function to grab the weapons list from the .json and convert it to a python list of dictionaries
    areas = load_file("areas.json")
    if weapons['version'] != areas['version']:
        sys.exit("Critical Error: Core data file (weapons/areas) versions do not match! Endministrator, please update program from Github repo. If this error still occurs after doing so, please report the problem to me on Github.")
    elif not os.path.exists("matches.json"):
            print("Missing file for weapon/area matches, generating new file.")
            generate_matches()
            matches = load_file('matches.json')
    else:
        matches = load_file('matches.json')
    if matches['version'] != weapons['version']:
        print("Matches file out of date, refreshing.")
        generate_matches()
    print(format_weapons(weapons['data']))
    target_weapons = translate_user_weapon_input(input(f"Please input which weapon numbers you want to focus on, separated by commas.\nEX: '1, 5, 32' will request focus on {weapons['data'][0]['name']}, {weapons['data'][4]['name']}, and {weapons['data'][31]['name']}: "), weapons)
    all_cases = find_optimal_settings(matches, target_weapons)
    print(format_solution(all_cases, target_weapons))
main()