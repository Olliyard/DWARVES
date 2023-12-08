from datetime import datetime
import time
import json
from master import Master
import os
LOCAL_PATH = os.getcwd() + "/filesys/colonyData.json"
# ANSI color codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
NC = '\033[0m'  # No color, to reset

class UI:
    def __init__(self):
        self.master = Master(1)
        # Temperature limits
        self.min_temperature = 15
        self.max_temperature = 30
        # Light intensity limits
        self.min_light_intensity = 0
        self.max_light_intensity = 100
        # Daytime hours limits
        self.min_daytime_hours = 1
        self.max_daytime_hours = 24
        # Observation interval limits
        self.min_observation_interval = 1
        self.max_observation_interval = 24
        self.clearInactiveEntries()
        self.loadColonyData()

    def clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
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

    def displayMainMenu(self):
        self.clearScreen()
        print("Options:")
        print("1. Check Colonies")
        print("2. Insert New Colony")
        print("3. Withdraw Old Colony")
        print("4. Check Out-of-bounds Settings")
        print("5. Pause/Resume Experiments")
        print("0. Quit")

    def listColonies(self):
        self.clearScreen()
        self.clearInactiveEntries()
        print("Currently active colonies")
        with open('filesys/colonyData.json', 'r') as file:
            data = json.load(file)
            colony_ids = list(data.keys())  # Store the actual colony IDs
            for i, colony_id in enumerate(colony_ids, start=1):
                print(f"{i}. {colony_id}")
            print("0. Back to main menu")

        # Return the list of colony IDs
        return colony_ids

    def displayColonyData(self, colonyID):
        self.master.updateColony(colonyID, None, True)
        self.master.getObservationData(colonyID)
        with open(f'{LOCAL_PATH}', 'r') as file:
            data = json.load(file)
            self.clearScreen()
            print(f"Colony Data for colony{colonyID}:")
            print(json.dumps(data[f"colony{colonyID}"], indent=4))

    def updateColonySettings(self, colonyID):
        with open('filesys/colonyData.json', 'r') as file:
            data = json.load(file)

            self.clearScreen()
            print(f"Colony Data for colony{colonyID}:")
            print(json.dumps(data[f"colony{colonyID}"], indent=4))

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

            while True:
                choice = input("Enter your choice: ")
                if choice in settings_mapping:
                    setting_key, setting_name = settings_mapping[choice]
                    new_value = input(f"Enter new {setting_name}: ")

                    if new_value.isnumeric():
                        new_value = int(new_value)
                        min_limit, max_limit = self.getLimits(setting_key)  # Implement getLimits function

                        if min_limit <= new_value <= max_limit:
                            data[f"colony{colonyID}"][setting_key] = new_value
                            with open('filesys/settings.json', 'w') as file:
                                json.dump(data, file, indent=4)
                            print(f"{GREEN}{setting_name} changed successfully!{NC}")
                            break  # Exit the loop if the value is accepted
                        else:
                            print(f"{RED}Invalid {setting_name}!{NC}")
                    else:
                        print(f"{RED}Invalid {setting_name}!{NC}")
                elif choice == '0':
                    print("Returning to main menu...")
                    break  # Exit the loop if the user chooses to go back
                else:
                    print(f"{RED}Invalid choice!{NC}")

    def getLimits(self, setting_key):
        # Return the limits for the specified setting
        if setting_key == 'daytime_temperature' or setting_key == 'nighttime_temperature':
            return self.min_temperature, self.max_temperature
        elif setting_key == 'daytime_red_light' or setting_key == 'nighttime_red_light' or setting_key == 'daytime_blue_light' or setting_key == 'nighttime_blue_light':
            return self.min_light_intensity, self.max_light_intensity
        elif setting_key == 'daytime_hours' or setting_key == 'nighttime_hours':
            return self.min_daytime_hours, self.max_daytime_hours
        elif setting_key == 'observation_interval':
            return self.min_observation_interval, self.max_observation_interval
        else:
            return None, None

# Insert colony into the system, and add it to the colonyData.json file
    def insertColony(self):
        self.clearScreen()
        # Check if no colonies are available
        if self.master.getAvailability() == 0:
            self.clearScreen()
            print("All colonies are occupied. Withdraw an old colony first.")
            input("Press Enter to continue...")
        else:
            self.clearScreen()
            print(self.master.getAvailability())
            colony_choice = input("Enter the number of the colony to insert (or 0 to go back): ")
            if colony_choice != '0':
                print(f'Inserting colony{colony_choice}')
                colony_id = int(colony_choice)
                self.master.insertColony(colony_id)       # Insert the colony into the Master instance
                self.master.getObservationData(colony_id) # Get observation data for the colony
                time.sleep(1)
                print("Colony inserted successfully!")
            else:
                print("Returning to main menu...")

# Extract colony from the system, and remove it from the colonyData.json file
    def extractColony(self):
        self.clearScreen()
        self.listColonies()
        colony_choice = input("Enter the number of the colony to extract (or 0 to go back): ")
        if colony_choice != '0':
            print(f'Extracting colony{colony_choice}')
            colony_id = int(colony_choice)
            
            # Extract the colony and remove it from the system
            if self.master.extractColony(colony_id):
                # Remove the colony from the colonyData.json file
                
                self.clearInactiveEntries(True)
                time.sleep(1)
                print(f"Colony{colony_id} extracted successfully!")
            else:
                print(f"ERROR: Unable to extract Colony{colony_id}.")
        else:
            print("Returning to main menu...")

# Remove inactive entries from the settings.json or colonyData.json files
    def clearInactiveEntries(self, extract=False):
        filename = f"{LOCAL_PATH}filesys/settings.json"

        try:
            with open(filename, "r") as file:
                try:
                    all_colonies_data = json.load(file)
                except json.JSONDecodeError:
                    all_colonies_data = {}
        except FileNotFoundError:
            all_colonies_data = {}

        active_colony_ids = set(map(str, self.master.colonyStorage.keys()))
        filtered_colonies_data = {key: value for key, value in all_colonies_data.items() if key[6:] in active_colony_ids}

        with open(filename, "w") as file:
            json.dump(filtered_colonies_data, file, indent=4)


# Load colony data from colonyData.json into the Master instance
    def loadColonyData(self):
        try:
            with open('filesys/colonyData.json', 'r') as file:
                colony_data = json.load(file)
                for colony_id, values in colony_data.items():
                    self.master.insertColony(int(colony_id[6:]))  # Extract colony number and insert into Master
                    self.master.updateColony(int(colony_id[6:]), values, True)  # Update colony data in Master
        except (FileNotFoundError, json.JSONDecodeError):
            self.master.logMessage(f"ALL: Unable to load colony data from filesys/colonyData.json")
  
# Main loop      
    def run(self):
        while True:
            self.displayMainMenu()
            choice = input("Enter your choice: ")

            if choice == '1':
                colony_ids = self.listColonies()                            # Get the list of colony IDs [colony1, colony2, ...]
                colony_ids = [colony_id[6:] for colony_id in colony_ids]    # Remove the 'colony' prefix [1, 2, ...]
                colony_choice = input("Enter your choice: ")
                if colony_choice != '0':
                    actual_colonyID = colony_ids[int(colony_choice) - 1]    # Subtract 1 to get the index
                    self.displayColonyData(actual_colonyID)                 # Display the colony data
                    action = input("1. Change settings \n0. Back to the main menu: ")
                    if action == '1':
                        self.updateColonySettings(actual_colonyID)          # Update the colony settings

                else:
                    print("Returning to the main menu...")

            elif choice == '2':
                # Insert colony into system
                self.insertColony()

            elif choice == '3':
                # Extract colony from system
                self.extractColony()
        

            elif choice == '0':
                print("Quitting...")
                break
            else:
                print("Invalid choice! Please enter a valid option.")

if __name__ == "__main__":
    ui = UI()
    ui.run()
