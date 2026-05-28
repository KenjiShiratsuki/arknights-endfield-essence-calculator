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
        w_list.append(weapons[(weapon-1)])
    return w_list

def find_optimal_settings(areas, matches, weapons, target_weapons):
    all_cases = {}
    for area in matches['data'].keys():
        area_weapons = matches['data'][area]['Valid Weapons']
        target_attributes = []
        target_skills = []
        target_stats = []
        for weapon in target_weapons:
            if weapon in area_weapons:
                if weapon.get('attribute') not in target_attributes: target_attributes.append(weapon.get('attribute'))
                if weapon.get('skill') not in target_skills: target_skills.append(weapon.get('skill'))
                if weapon.get('stat') not in target_stats: target_stats.append(weapon.get('stat'))
        while target_attributes < 3:
            target_attributes.append('free')
        for combo in combinations(target_attributes, 3):
            for skill in target_skills:
                count = 0
                case_key = f"{area} | {combo} | {skill}"
                matching_weapon_list = []
                for weapon in target_weapons:
                    if all(weapon.get('attribute') in combo, weapon.get('skill') == skill):
                        count += 1
                        all_cases[case_key] = {'count': count, 'weapons': matching_weapon_list}


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
    find_optimal_settings(areas, matches, weapons, target_weapons)
main()