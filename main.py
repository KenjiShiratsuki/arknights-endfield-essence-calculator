import json

def load_weapons(filename):
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

def main():
    weapons = load_weapons("weapons.json") #calls the function to grab the weapons list from the .json and convert it to a python list of dictionaries
    print(format_weapons(weapons))
    target_weapons = translate_user_weapon_input(input(f"Please input which weapon numbers you want to focus on, separated by commas.\nEX: '1, 5, 32' will request focus on {weapons[0]['name']}, {weapons[4]['name']}, and {weapons[31]['name']}: "), weapons)
    print(target_weapons)
main()