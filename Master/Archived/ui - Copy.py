from datetime import datetime
import time
import json
from master import Master
import os
LOCAL_PATH = os.path.join(os.getcwd(), "filesys", "colonyData.json")
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
        with open(f'{LOCAL_PATH}', 'r') as file:
            data = json.load(file)
            colonyIDs = list(data.keys())  # Store the actual colony IDs
            for i, colonyID in enumerate(colonyIDs, start=1):
                print(f"{i}. {colonyID}")
            print("0. Back to main menu")

        # Return the list of colony IDs
        return colonyIDs

    def displayColonyData(self, colonyID):
        self.master.updateColony(colonyID, None, True)
        self.master.getObservationData(colonyID)
        with open(f'{LOCAL_PATH}', 'r') as file:
            data = json.load(file)
            self.clearScreen()
            print(f"Colony Data for colony{colonyID}:")
            print(json.dumps(data[f"colony{colonyID}"], indent=4))

    # Update the settings for the specified colony
    def updateColonySettings(self, colonyID):
        # Get the colony data from the Master instance
        updated_colony = self.master.colonyStorage[colonyID]

        while True:
            self.clearScreen()
            print(f"Changing settings for {updated_colony}:")

            # Display daytime settings
            print(f"Daytime Settings:")
            print(f"1. Daytime temperature: {updated_colony.dayTemp} (Limit: {self.min_temperature}-{self.max_temperature}°C)")
            print(f"2. Daytime red light: {updated_colony.redDay} (Limit: {self.min_light_intensity}-{self.max_light_intensity})")
            print(f"3. Daytime blue light: {updated_colony.blueDay} (Limit: {self.min_light_intensity}-{self.max_light_intensity})")
            print(f"4. Daytime hours: {updated_colony.dayInterval.hour} (Limit: {self.min_daytime_hours}-{self.max_daytime_hours} hours)")

            # Display nighttime settings
            print(f"Nighttime Settings:")
            print(f"5. Nighttime temperature: {updated_colony.nightTemp} (Limit: {self.min_temperature}-{self.max_temperature}°C)")
            print(f"6. Nighttime red light: {updated_colony.redNight} (Limit: {self.min_light_intensity}-{self.max_light_intensity})")
            print(f"7. Nighttime blue light: {updated_colony.blueNight} (Limit: {self.min_light_intensity}-{self.max_light_intensity})")

            # Display Observation interval setting
            print(f"Observation Settings:")
            print(f"8. Observation interval: {self.master.observationFrequency} (Limit: {self.min_observation_interval}-{self.max_observation_interval} hours)")
            print("0. Back to main menu")

            setting_choice = input("Enter the setting to change (or 0 to go back): ")

            if setting_choice == '0':
                break
            elif setting_choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                new_value = input("Enter the new value: ")

                try:
                    new_value = int(new_value)
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    input("Press Enter to continue...")
                    continue

                min_limit, max_limit = self.getLimits(setting_choice)

                if min_limit <= new_value <= max_limit:
                    setting_key = self.getSettingKey(setting_choice)
                    # Update the colony settings directly
                    setattr(updated_colony, setting_key, new_value)
                    print(f"Setting updated. New value for {setting_key}: {getattr(updated_colony, setting_key)}")

                    # Add the following print statement to check the attribute names in the Colony instance
                    print(f"Attributes in updated_colony: {dir(updated_colony)}")

                    # Update the JSON file with the new setting
                    with open(LOCAL_PATH, 'r') as f:
                        settings = json.load(f)

                    colony_settings = settings.get(f'colony{colonyID}', {})
                    colony_settings[setting_key] = new_value
                    settings[f'colony{colonyID}'] = colony_settings

                    with open(LOCAL_PATH, 'w') as f:
                        json.dump(settings, f, indent=4)
                    input("Press Enter to continue...")
                else:
                    print(f"Invalid input. Value must be between {min_limit} and {max_limit}.")
                    input("Press Enter to continue...")
            else:
                print("Invalid choice. Please select a valid option.")
                input("Press Enter to continue...")

    # Save colony data to colonyData.json
    def saveColonyData(self):
        with open(LOCAL_PATH, 'r') as f:
            settings = json.load(f)

        for colonyID, colony_instance in self.colonyStorage.items():
            colony_data = settings.get(f'colony{colonyID}', {})
            for attribute, value in colony_instance.__dict__.items():
                colony_data[attribute] = value

            settings[f'colony{colonyID}'] = colony_data

        with open(LOCAL_PATH, 'w') as f:
            json.dump(settings, f, indent=4)

    # Return the limits for the specified setting
    def getLimits(self, setting_choice):
        if setting_choice == '1' or setting_choice == '5':
            return self.min_temperature, self.max_temperature
        elif setting_choice in ['2', '3', '4', '6', '7']:
            return self.min_light_intensity, self.max_light_intensity
        elif setting_choice in ['8']:
            return self.min_observation_interval, self.max_observation_interval
        else:
            return None, None

    # Add this method to your UI class
    def getSettingKey(self, setting_choice):
        setting_key_mapping = {
            '1': 'dayTemp',
            '2': 'redDay',
            '3': 'blueDay',
            '4': 'dayInterval',
            '5': 'nightTemp',
            '6': 'redNight',
            '7': 'blueNight',
            '8': 'observationInterval',  # Adjusted to match your Colony class attribute
        }
        return setting_key_mapping.get(setting_choice)

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
                colonyID = int(colony_choice)
                self.master.insertColony(colonyID)       # Insert the colony into the Master instance
                self.master.getObservationData(colonyID) # Get observation data for the colony
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
            colonyID = int(colony_choice)
            
            # Extract the colony and remove it from the system
            if self.master.extractColony(colonyID):
                # Remove the colony from the colonyData.json file
                
                self.clearInactiveEntries()
                time.sleep(1)
                print(f"Colony{colonyID} extracted successfully!")
            else:
                print(f"ERROR: Unable to extract Colony{colonyID}.")
        else:
            print("Returning to main menu...")

    # Remove extracted entries from the colonyData.json
    def clearInactiveEntries(self):
        try:
            with open(LOCAL_PATH, "r") as file:
                try:
                    all_colonies_data = json.load(file)
                except json.JSONDecodeError:
                    all_colonies_data = {}
        except FileNotFoundError:
            all_colonies_data = {}

        active_colonyIDs = set(map(str, self.master.colonyStorage.keys()))
        filtered_colonies_data = {key: value for key, value in all_colonies_data.items() if key[6:] in active_colonyIDs}

        with open(LOCAL_PATH, "w") as file:
            json.dump(filtered_colonies_data, file, indent=4)

    # Load colony data from colonyData.json into the Master instance
    def loadColonyData(self):
        try:
            with open(LOCAL_PATH, 'r') as file:
                updated_colony = json.load(file)
                for colonyID, values in updated_colony.items():
                    colony_number = int(colonyID.split("colony")[1])  # Extract colony number
                    self.master.insertColony(colony_number)  # Insert colony into Master
                    self.master.updateColony(colony_number, values, True)  # Update colony data in Master
        except (FileNotFoundError, json.JSONDecodeError):
            self.master.logMessage(f"ALL: Unable to load colony data from {LOCAL_PATH}")


    # Check if settings in colonyData.json are out of bounds
    def checkOutOfBoundsSettings(self):
        # Check if settings in colonyData.json are out of bounds
        self.clearScreen()
        print("Checking out-of-bounds settings...")
        # Loop through all current colonies and check if their settings are out of bounds. If they are, print a warning message if otherwise, print a success message
        with open(f'{LOCAL_PATH}', 'r') as file:
            data = json.load(file)
            for colony, info in data.items():
                out_of_bounds = False  # Flag to track if any setting is out of bounds
                colony_name = colony
                # Check each setting
                if not (self.min_temperature <= info['daytime_temperature'] <= self.max_temperature):
                    print(f"Colony {colony_name} has out-of-bounds daytime temperature: {info['daytime_temperature']} (Limit: {self.min_temperature}-{self.max_temperature}°C)")
                    out_of_bounds = True

                if not (self.min_temperature <= info['nighttime_temperature'] <= self.max_temperature):
                    print(f"Colony {colony_name} has out-of-bounds nighttime temperature: {info['nighttime_temperature']} (Limit: {self.min_temperature}-{self.max_temperature}°C)")
                    out_of_bounds = True

                if not (self.min_light_intensity <= info['daytime_red_light'] <= self.max_light_intensity):
                    print(f"Colony {colony_name} has out-of-bounds daytime red light: {info['daytime_red_light']} (Limit: {self.min_light_intensity}-{self.max_light_intensity})")
                    out_of_bounds = True

                if not (self.min_light_intensity <= info['daytime_blue_light'] <= self.max_light_intensity):
                    print(f"Colony {colony_name} has out-of-bounds daytime blue light: {info['daytime_blue_light']} (Limit: {self.min_light_intensity}-{self.max_light_intensity})")
                    out_of_bounds = True

                if not (self.min_light_intensity <= info['nighttime_red_light'] <= self.max_light_intensity):
                    print(f"Colony {colony_name} has out-of-bounds nighttime red light: {info['nighttime_red_light']} (Limit: {self.min_light_intensity}-{self.max_light_intensity})")
                    out_of_bounds = True

                if not (self.min_light_intensity <= info['nighttime_blue_light'] <= self.max_light_intensity):
                    print(f"Colony {colony_name} has out-of-bounds nighttime blue light: {info['nighttime_blue_light']} (Limit: {self.min_light_intensity}-{self.max_light_intensity})")
                    out_of_bounds = True

                try:
                    daytime_hours = int(info['daytime_hours'].split(':')[0])
                    if not (self.min_daytime_hours <= daytime_hours <= self.max_daytime_hours):
                        print(f"Colony {colony_name} has out-of-bounds daytime hours: {daytime_hours} (Limit: {self.min_daytime_hours}-{self.max_daytime_hours} hours)")
                        out_of_bounds = True
                except ValueError:
                    print(f"Colony {colony_name} has an invalid format for daytime hours.")
                    out_of_bounds = True

                if not (self.min_observation_interval <= int(info['observation_interval']) <= self.max_observation_interval):
                    print(f"Colony {colony_name} has out-of-bounds observation interval: {info['observation_interval']} (Limit: {self.min_observation_interval}-{self.max_observation_interval} hours)")
                    out_of_bounds = True

                if out_of_bounds:
                    print()
                else:
                    print(f"Colony {colony_name}: All settings are within bounds")
                    
            input("Press Enter to continue...")


    # Main loop      
    def run(self):
        while True:
            self.displayMainMenu()
            choice = input("Enter your choice: ")

            if choice == '1':
                colonyIDs = self.listColonies()                            # Get the list of colony IDs [colony1, colony2, ...]
                colonyIDs = [colonyID[6:] for colonyID in colonyIDs]    # Remove the 'colony' prefix [1, 2, ...]
                colony_choice = input("Enter your choice: ")
                if colony_choice != '0':
                    actual_colonyID = colonyIDs[int(colony_choice) - 1]    # Subtract 1 to get the index
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
            
            elif choice == '4':
                # Check out-of-bounds settings
                self.checkOutOfBoundsSettings()
            
            elif choice == '5':
                pass

            elif choice == '0':
                print("Quitting...")
                break
            else:
                print("Invalid choice! Please enter a valid option.")

if __name__ == "__main__":
    ui = UI()
    ui.run()
