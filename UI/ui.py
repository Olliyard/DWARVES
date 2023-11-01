import json
from datetime import datetime

# Settings limits
# Temperature limits
min_temperature = 15
max_temperature = 30
# Light intensity limits
min_light_intensity = 0
max_light_intensity = 1
# Daytime hours limits
min_daytime_hours = 1
max_daytime_hours = 24
# Observation interval limits
min_observation_interval = 1
max_observation_interval = 24

# ANSI color codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
NC = '\033[0m'  # No color, to reset

# Function to clear the screen and display the ASCII art
def clear_screen():
    print("\033c")
    print(f"{GREEN}")
    print(r"""
$$$$$$$\  $$\      $$\  $$$$$$\  $$$$$$$\  $$\    $$\ $$$$$$$$\  $$$$$$\        $$\   $$\ $$$$$$\ 
$$  __$$\ $$ | $\  $$ |$$  __$$\ $$  __$$\ $$ |   $$ |$$  _____|$$  __$$\       $$ |  $$ |\_$$  _|
$$ |  $$ |$$ |$$$\ $$ |$$ /  $$ |$$ |  $$ |$$ |   $$ |$$ |      $$ /  \__|      $$ |  $$ |  $$ |  
$$ |  $$ |$$ $$ $$\$$ |$$$$$$$$ |$$$$$$$  |\$$\  $$  |$$$$$\    \$$$$$$\        $$ |  $$ |  $$ |  
$$ |  $$ |$$$$  _$$$$ |$$  __$$ |$$  __$$<  \$$\$$  / $$  __|    \____$$\       $$ |  $$ |  $$ |  
$$ |  $$ |$$$  / \$$$ |$$ |  $$ |$$ |  $$ |  \$$$  /  $$ |      $$\   $$ |      $$ |  $$ |  $$ |  
$$$$$$$  |$$  /   \$$ |$$ |  $$ |$$ |  $$ |   \$  /   $$$$$$$$\ \$$$$$$  |      \$$$$$$  |$$$$$$\ 
\_______/ \__/     \__|\__|  \__|\__|  \__|    \_/    \________| \______/        \______/ \______|

    """)
    print(f"{NC}")  # Reset color

# Function to check colonies
def check_colonies():
    clear_screen()
    print("Checking colonies...")
    with open('settings.json', 'r') as file:
        data = json.load(file)
        i = 1 # to skip the loading zone
        for colony in data:
            if colony != 'loadingZone':
                print(f"{i}. {colony}")
                i += 1
    print("0. Back to main menu")


# Function to display JSON data for a specific colony
def display_colony_data(colony_name):
    with open('settings.json', 'r') as file:
        data = json.load(file)
        clear_screen()
        print(f"Colony Data for {colony_name}:")
        print(json.dumps(data[colony_name], indent=4))

# Function to change specific settings for a colony
def change_colony_settings(colony_name):
    while True:
        clear_screen()
        with open('settings.json', 'r+') as file:
            data = json.load(file)
            colony_data = data[colony_name]
            print(f"Changing settings for Colony {colony_name}:")

            # Display daytime settings
            print(f"Daytime Settings:")
            print(f"1. Daytime temperature: {colony_data['daytime_temperature']} (Limit: {min_temperature}-{max_temperature}°C)")
            print(f"2. Daytime light intensity: {colony_data['daytime_light_intensity']} (Limit: {min_light_intensity}-{max_light_intensity})")
            print(f"3. Daytime hours: {colony_data['daytime_hours']} (Limit: {min_daytime_hours}-{max_daytime_hours} hours)")

            # Display nighttime settings
            print(f"Nighttime Settings:")
            print(f"4. Nighttime temperature: {colony_data['nighttime_temperature']} (Limit: {min_temperature}-{max_temperature}°C)")
            print(f"5. Nighttime light intensity: {colony_data['nighttime_light_intensity']} (Limit: {min_light_intensity}-{max_light_intensity})")

            # Display Observation interval setting
            print(f"Observation Settings:")
            print(f"6. Observation interval: {colony_data['observation_interval']} (Limit: {min_observation_interval}-{max_observation_interval} hours)")

            print("0. Back to main menu")
            setting_choice = input("Enter the setting to change (or 0 to go back): ")

            if setting_choice == '0':
                break
            elif setting_choice in ['1', '2', '3', '4', '5', '6']:
                new_value = input(f"Enter the new {'Daytime temperature' if setting_choice == '1' else 'Daytime light intensity' if setting_choice == '2' else 'Daytime hours' if setting_choice == '3' else 'Nighttime temperature' if setting_choice == '4' else 'Nighttime light intensity' if setting_choice == '5' else 'Observation interval'}: ")

                try:
                    new_value = int(new_value)
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    input("Press Enter to continue...")
                    continue

                if setting_choice == '1':
                    if min_temperature <= new_value <= max_temperature:
                        colony_data['daytime_temperature'] = new_value
                    else:
                        print(f"Invalid input. Temperature must be between {min_temperature} and {max_temperature}°C.")
                        input("Press Enter to continue...")
                elif setting_choice == '2':
                    if min_light_intensity <= new_value <= max_light_intensity:
                        colony_data['daytime_light_intensity'] = new_value
                    else:
                        print(f"Invalid input. Light intensity must be between {min_light_intensity} and {max_light_intensity}.")
                        input("Press Enter to continue...")
                elif setting_choice == '3':
                    if min_daytime_hours <= new_value <= max_daytime_hours:
                        colony_data['daytime_hours'] = new_value
                    else:
                        print(f"Invalid input. Daytime hours must be between {min_daytime_hours} and {max_daytime_hours} hours.")
                        input("Press Enter to continue...")
                elif setting_choice == '4':
                    if min_temperature <= new_value <= max_temperature:
                        colony_data['nighttime_temperature'] = new_value
                    else:
                        print(f"Invalid input. Temperature must be between {min_temperature} and {max_temperature}°C.")
                        input("Press Enter to continue...")
                elif setting_choice == '5':
                    if min_light_intensity <= new_value <= max_light_intensity:
                        colony_data['nighttime_light_intensity'] = new_value
                    else:
                        print(f"Invalid input. Light intensity must be between {min_light_intensity} and {max_light_intensity}.")
                        input("Press Enter to continue...")
                elif setting_choice == '6':
                    if min_observation_interval <= new_value <= max_observation_interval:
                        colony_data['observation_interval'] = new_value
                    else:
                        print(f"Invalid input. Observation interval must be between {min_observation_interval} and {max_observation_interval} hours.")
                        input("Press Enter to continue...")

                # Write the updated data back to the file
                file.seek(0)
                file.truncate()
                json.dump(data, file, indent=4)
                
            else:
                print("Invalid choice. Please select a valid option.")

# Function to insert a new colony
def insert_new_colony():
    with open('settings.json', 'r') as file:
        data = json.load(file)
        # Check if the loading zone is occupied
        loading_zone_occupied = data['loadingZone']['occupied']

        if loading_zone_occupied == False:
            clear_screen()
            print("The loading zone is empty. Enter a colony first.")
            input("Press Enter to continue...")
        # Check if no colonies are available
        elif all(value['occupied'] for value in data.values() if value != data['loadingZone']):
            clear_screen()
            print("All colonies are occupied. Withdraw an old colony first.")
            input("Press Enter to continue...")
        else:
            clear_screen()
            print("Available non-occupied colonies:")
            available_colonies = [key for key, value in data.items() if not value['occupied']]
            for i, colony in enumerate(available_colonies, 1):
                print(f"{i}. {colony}")
            print("0. Back to main menu")

            colony_choice = input("Enter the number of the colony to insert (or 0 to go back): ")
            if colony_choice != '0':
                colony_choice = int(colony_choice)
                if 1 <= colony_choice <= len(available_colonies):
                    colony_name = available_colonies[colony_choice - 1]
                    data[colony_name]['occupied'] = True
                    data[colony_name]['experiment_start_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    data['loadingZone']['occupied'] = False                    

                    with open('settings.json', 'w') as outfile:
                        json.dump(data, outfile, indent=4)

                    clear_screen()
                    print(f"Colony {colony_name} with ID: {data[colony_name]['id']} has been marked as occupied. Loading zone is now free.")
                    input("Press Enter to continue...")

# Function to withdraw an old colony
def withdraw_old_colony():
    with open('settings.json', 'r') as file:
        data = json.load(file)
        # Check if the loading zone is occupied
        loading_zone_occupied = data['loadingZone']['occupied']

        if loading_zone_occupied:
            clear_screen()
            print("Loading zone is not empty. Remove the colony first.")
            input("Press Enter to continue...")
        # Check if no colonies are occupied
        elif all(value['occupied'] == False for value in data.values() if value != data['loadingZone']):
            clear_screen()
            print("No colonies are occupied. Insert a colony first.")
            input("Press Enter to continue...")
        else:
            clear_screen()
            print("Occupied colonies:")
            occupied_colonies = [key for key, value in data.items() if key != 'loadingZone' and value['occupied']]
            for i, colony in enumerate(occupied_colonies, 1):
                print(f"{i}. {colony}")
            print("0. Back to main menu")

            colony_choice = input("Enter the number of the colony to withdraw (or 0 to go back): ")
            if colony_choice != '0':
                colony_choice = int(colony_choice)
                if 1 <= colony_choice <= len(occupied_colonies):
                    colony_name = occupied_colonies[colony_choice - 1]
                    data[colony_name]['occupied'] = False
                    data[colony_name]['experiment_start_date'] = None
                    
                    data['loadingZone']['occupied'] = True

                    with open('settings.json', 'w') as outfile:
                        json.dump(data, outfile, indent=4)

                    print(f"Colony {colony_name} has been withdrawn and the loading zone is now occupied.")
                    input("Press Enter to continue...")

# Function to check and report colonies with out-of-bounds settings
def check_out_of_bounds_settings():
    clear_screen()
    print("Checking colonies for out-of-bounds settings...")
    with open('settings.json', 'r') as file:
        data = json.load(file)
        for colony, info in data.items():
            if colony != 'loadingZone':
                out_of_bounds = False  # Flag to track if any setting is out of bounds
                colony_name = colony

                # Check each setting
                if not (min_temperature <= info['daytime_temperature'] <= max_temperature):
                    print(f"Colony {colony_name} has out-of-bounds daytime temperature: {info['daytime_temperature']} (Limit: {min_temperature}-{max_temperature}°C)")
                    out_of_bounds = True

                if not (min_temperature <= info['nighttime_temperature'] <= max_temperature):
                    print(f"Colony {colony_name} has out-of-bounds nighttime temperature: {info['nighttime_temperature']} (Limit: {min_temperature}-{max_temperature}°C)")
                    out_of_bounds = True

                if not (min_light_intensity <= info['daytime_light_intensity'] <= max_light_intensity):
                    print(f"Colony {colony_name} has out-of-bounds daytime light intensity: {info['daytime_light_intensity']} (Limit: {min_light_intensity}-{max_light_intensity})")
                    out_of_bounds = True
                
                if not (min_light_intensity <= info['nighttime_light_intensity'] <= max_light_intensity):
                    print(f"Colony {colony_name} has out-of-bounds nighttime light intensity: {info['nighttime_light_intensity']} (Limit: {min_light_intensity}-{max_light_intensity})")
                    out_of_bounds = True

                if not (min_daytime_hours <= info['daytime_hours'] <= max_daytime_hours):
                    print(f"Colony {colony_name} has out-of-bounds daytime hours: {info['daytime_hours']} (Limit: {min_daytime_hours}-{max_daytime_hours} hours)")
                    out_of_bounds = True

                if not (min_observation_interval <= info['observation_interval'] <= max_observation_interval):
                    print(f"Colony {colony_name} has out-of-bounds observation interval: {info['observation_interval']} (Limit: {min_observation_interval}-{max_observation_interval} hours)")
                    out_of_bounds = True

                if out_of_bounds:
                    print()
                else:
                    print(f"Colony {colony_name}: All settings are within bounds")
        input("Press Enter to continue...")


# Main menu
while True:
    clear_screen()
    print("Options:")
    print("1. Check colonies")
    print("2. Insert New colony")
    print("3. Withdraw old Colony")
    print("4. Check Out-of-bounds Settings")
    print("0. Quit")

    choice = input("Enter your choice: ")

    if choice == '1':
        check_colonies()
        colony_choice = input("Enter the number of the colony to view details or change settings (0 to go back to the main menu): ")
        if colony_choice != '0':
            with open('settings.json', 'r') as file:
                data = json.load(file)
                colonies = [colony for colony in data.keys() if colony != 'loadingZone']
                colony_choice = int(colony_choice)
                if 1 <= colony_choice <= len(colonies):
                    colony_name = colonies[colony_choice - 1]
                    display_colony_data(colony_name)
                    action = input("1. Change settings \n0. Back to the main menu: ")
                    if action == '1':
                        change_colony_settings(colony_name)
    elif choice == '2':
        insert_new_colony()
    elif choice == '3':
        withdraw_old_colony()
    elif choice == '4':
        check_out_of_bounds_settings()
    elif choice == '0':
        clear_screen()
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please select a valid option.")
        input("Press Enter to continue...")
