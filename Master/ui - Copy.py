import json
from datetime import datetime
import time
from master import Master

# Settings limits
# Temperature limits
min_temperature = 15
max_temperature = 30
# Light intensity limits
min_light_intensity = 0
max_light_intensity = 100
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
def clearScreen():
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
    Version 1.0
    """)
    print(f"{NC}")  # Reset color

# Function to check colonies present in the system
def listColonies():
    clearScreen()
    print("Currently active colonies")
    with open('filesys/colonyData.json', 'r') as file:
        data = json.load(file)
        i = 1 
        for colony in data:
            print(f"{i}. {colony}")
            i += 1
    print("0. Back to main menu")

# Function to display JSON data for a specific colony
def displayColonyData(colony_id, master):
    master.updateColony(colony_id, None, True)
    with open('filesys/colonyData.json', 'r') as file:
        data = json.load(file)
        clearScreen()
        print(f"Colony Data for colony{colony_id}:")
        print(json.dumps(data[f"colony{colony_id}"], indent=4))

def changeSettings(colony_id):
    with open('filesys/colonyData.json', 'r') as file:
        data = json.load(file)
        clearScreen()
        print(f"Colony Data for colony{colony_id}:")
        print(json.dumps(data[f"colony{colony_id}"], indent=4))

        settings_mapping = {
            '1': ('daytime_temperature', 'Daytime temperature'),
            '2': ('nighttime_temperature', 'Nighttime temperature'),
            '3': ('daytime_red_light', 'Daytime red light intensity'),
            '4': ('nighttime_red_light', 'Nighttime red light intensity'),
            '5': ('daytime_blue_light', 'Daytime blue light intensity'),
            '6': ('nighttime_blue_light', 'Nighttime blue light intensity'),
            '7': ('daytime_hours', 'Daytime hours'),
            '8': ('nighttime_hours', 'Nighttime hours'),
            '9': ('observation_interval', 'Observation interval'),
        }

        choice = input("Enter your choice: ")
        if choice in settings_mapping:
            setting_key, setting_name = settings_mapping[choice]
            new_value = input(f"Enter new {setting_name}: ")

            if new_value.isnumeric():
                new_value = int(new_value)
                min_limit, max_limit = getLimits(setting_key)  # Implement get_limits function

                if min_limit <= new_value <= max_limit:
                    data[f"colony{colony_id}"][setting_key] = new_value
                    with open('filesys/settings.json', 'w') as file:
                        json.dump(data, file, indent=4)
                    print(f"{GREEN}{setting_name} changed successfully!{NC}")
                else:
                    print(f"{RED}Invalid {setting_name}!{NC}")
            else:
                print(f"{RED}Invalid {setting_name}!{NC}")
        elif choice == '0':
            print("Returning to main menu...")
        else:
            print(f"{RED}Invalid choice!{NC}")

def getLimits(setting_key):
    # Return the limits for the specified setting
    if setting_key == 'daytime_temperature' or setting_key == 'nighttime_temperature':
        return min_temperature, max_temperature
    elif setting_key == 'daytime_red_light' or setting_key == 'nighttime_red_light' or setting_key == 'daytime_blue_light' or setting_key == 'nighttime_blue_light':
        return min_light_intensity, max_light_intensity
    elif setting_key == 'daytime_hours' or setting_key == 'nighttime_hours':
        return min_daytime_hours, max_daytime_hours
    elif setting_key == 'observation_interval':
        return min_observation_interval, max_observation_interval
    else:
        return None, None

def insertColonyUI():
    clearScreen()
    with open('filesys/settings.json', 'r') as file:
        data = json.load(file)

        # Check if no colonies are available
        if master.getAvailability() == 0:
            clearScreen()
            print("All colonies are occupied. Withdraw an old colony first.")
            input("Press Enter to continue...")
        else:
            clearScreen()
            print(master.getAvailability())
            colony_choice = input("Enter the number of the colony to insert (or 0 to go back): ")
            if colony_choice != '0':
                selected_colony = f"colony{colony_choice}"
                if selected_colony in data:
                    print("Colony ID: ", colony_choice)
                    time.sleep(1)
                    return int(colony_choice)
                else:
                    print(f"Invalid colony selection: {colony_choice}")
                    time.sleep(1)
            else:
                print("Returning to the main menu...")
                time.sleep(1)
    return 0  # Or handle this case appropriately




# Create an instance of the Master class
master = Master(1)

while True:
    clearScreen()
    
    # Display main menu
    print("Options:")
    print("1. Check colonies")
    print("2. Insert New colony")
    print("3. Withdraw old Colony")
    print("4. Check Out-of-bounds Settings")
    print("5. Pause/Resume experiments")
    print("0. Quit")
    
    choice = input("Enter your choice: ")

    if choice == '1':
        listColonies()
        colony_id = input("Enter your choice: ")
        if colony_id != '0':
            colony_id = int(colony_id)
            master.getObservationData(colony_id)
            displayColonyData(f"colony{colony_id}", master)
            action = input("1. Change settings \n0. Back to the main menu: ")
            if action == '1':
                changeSettings(colony_id)
                
        else:
            print("Returning to main menu...")
            
    elif choice == '2':
        colonyID = insertColonyUI()
        print("Colony ID: ", colonyID)
        colony = master.insertColony(colonyID)
        