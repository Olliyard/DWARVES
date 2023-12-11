from datetime import datetime
import threading
import time
import json
from master import Master
import os

JSON_PATH = os.path.join(os.getcwd(), "filesys", "colonyData.json")
IMAGE_PATH = os.path.join(os.getcwd(), "images")
# ANSI color codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
NC = '\033[0m'  # No color, to reset

class UI:
    def __init__(self):
        self.master = Master()
        self.__updateMaster()
        
        # Threading to run observations independently from the UI
        self.scheduler = threading.Thread(target=self.master.startObservationScheduler, daemon=True)
        self.scheduler.start()
        
        # Temperature limits
        self.minTemp = 15
        self.maxTemp = 30
        # Light intensity limits
        self.minLight = 0
        self.maxLight = 100
        # Daytime hours limits
        self.minDay = datetime.strptime("00:00:00", "%H:%M:%S").time()
        self.maxDay = datetime.strptime("23:59:59", "%H:%M:%S").time()
        # Nighttime hours limits
        self.minNight = datetime.strptime("00:00:00", "%H:%M:%S").time()
        self.maxNight = datetime.strptime("23:59:59", "%H:%M:%S").time()
        # Observation interval limits
        self.minObs = 1
        self.maxObs = 24

    # Main loop      
    def run(self):
        try:
            self.clearScreen()
            while True:
                self.displayMainMenu()
                choice = input("Enter your choice: ")
                
                # Insert colony
                if choice == "1":
                    self.clearScreen()
                    self.listColonies()
                    while True:
                        colonyID = input("Enter colony ID (0. Go back): ")

                        # Check if '0' is pressed to go back
                        if colonyID == '0':
                            break

                        if int(colonyID) in self.master.colonies:
                            print(f'{RED}Colony already exists!{NC}')
                        else:
                            break

                    # If '0' is pressed, go back to the main menu
                    if colonyID == '0':
                        continue
                    
                    if colonyID.isdigit():
                        colonyID = int(colonyID)
                        self.master.insertColony(colonyID)
                        self.master.getObservationData(colonyID)

                # Extract colony
                elif choice == "2":
                    self.clearScreen()
                    self.listColonies()
                    while True:
                        colonyID = input("Enter colony ID (0. Go back): ")

                        # Check if '0' is pressed to go back
                        if colonyID == '0':
                            break

                        if int(colonyID) not in self.master.colonies:
                            print(f'{RED}Colony does not exists!{NC}')
                        else:
                            break

                    # If '0' is pressed, go back to the main menu
                    if colonyID == '0':
                        continue
                    
                    if colonyID.isdigit():
                        colonyID = int(colonyID)
                        self.master.extractColony(colonyID)
                        self.master.getObservationData(colonyID)
    
                # View images
                elif choice == "3":
                    self.clearScreen()
                    self.listColonies()
                    while True:
                        colonyID = input("Enter colony ID (0. Go back): ")

                        # Check if '0' is pressed to go back
                        if colonyID == '0':
                            break

                        if int(colonyID) not in self.master.colonies:
                            print(f'{RED}Colony does not exists!{NC}')
                        else:
                            break

                    # If '0' is pressed, go back to the main menu
                    if colonyID == '0':
                        continue
                    
                    if colonyID.isdigit():
                        colonyID = int(colonyID)
                        self.showImages(colonyID)
                        self.master.getObservationData(colonyID)
    
                # Check colonies               
                elif choice == "4":
                    self.clearScreen()
                    self.listColonies()
                    while True:
                        colonyID = input("Enter colony ID (0. Go back): ")

                        # Check if '0' is pressed to go back
                        if colonyID == '0':
                            break

                        if int(colonyID) not in self.master.colonies:
                            print(f'{RED}Colony does not exists!{NC}')
                        else:
                            break
                    
                    # If '0' is pressed, go back to the main menu
                    if colonyID == '0':
                        continue
                    
                    self.clearScreen()
                    if colonyID.isdigit():
                        colonyID = int(colonyID)
                        print(self.master.colonies.get(colonyID))
                        # wait for user input before going to main menu
                        input("Press enter to continue...")

                # Change colony settings
                elif choice == "5":
                    self.clearScreen()
                    self.listColonies()
                    while True:
                        colonyID = input("Enter colony ID (0. Go back): ")

                        # Check if '0' is pressed to go back
                        if colonyID == '0':
                            break

                        if int(colonyID) not in self.master.colonies:
                            print(f'{RED}Colony does not exists!{NC}')
                        else:
                            break
                    
                    # If '0' is pressed, go back to the main menu
                    if colonyID == '0':
                        continue
                    
                    if colonyID.isdigit():
                        colonyID = int(colonyID)
                        self.changeColonySettings(colonyID)

                # Change observation interval
                elif choice == "6":
                    self.clearScreen()
                    print("Current observation interval:", self.master.observationFrequency)
                    while True:
                        newInterval = input("Enter new observation interval (0. Go back): ")

                        # Check if '0' is pressed to go back
                        if newInterval == '0':
                            break

                        if newInterval.isdigit():
                            newInterval = int(newInterval)
                            if self.minObs <= newInterval <= self.maxObs:
                                self.master.setObservationFrequency(newInterval)
                                print("New observation interval:", self.master.observationFrequency)
                                break
                            else:
                                print(f"{RED}Error: Invalid interval!{NC}")
                        else:
                            print(f"{RED}Error: Invalid interval!{NC}")

                # Check bound settings
                elif choice == "7":
                    self.clearScreen()
                    self.checkBoundSettings()
                    
                elif choice == "8":
                    self.clearScreen()
                    self.listColonies()
                    while True:
                        colonyID = input("Enter colony ID (0. Go back): ")

                        # Check if '0' is pressed to go back
                        if colonyID == '0':
                            break

                        if int(colonyID) not in self.master.colonies:
                            print(f'{RED}Colony does not exists!{NC}')
                        else:
                            break
                    if colonyID == '0':
                        continue
                    
                    if colonyID.isdigit():
                        colonyID = int(colonyID)
                        self.master.observeColony(colonyID)
                        self.master.getObservationData(colonyID)

                # Exit
                elif choice == "0":
                    break
                
                else:
                    print(f"{RED}Invalid input!{NC}")

            while True:
                time.sleep(1)  # Keep the main thread alive
        except KeyboardInterrupt:
            print("UI terminated.")

    # Check bound settings
    def checkBoundSettings(self):
        with open(JSON_PATH, 'r') as f:
            data = json.load(f)
            for name, colony in data.items():
                boundsFlag = False
                if not self.minTemp <= colony.get("dayTemperature", 15) <= self.maxTemp:
                    print(f"{RED}Error: Invalid day temperature for {name}{NC}")
                    boundsFlag = True
                if not self.minTemp <= colony.get("nightTemperature", 15) <= self.maxTemp:
                    print(f"{RED}Error: Invalid night temperature for {name}{NC}")
                    boundsFlag = True
                if not self.minLight <= colony.get("redDay", 0) <= self.maxLight:
                    print(f"{RED}Error: Invalid red day value for {name}{NC}")
                    boundsFlag = True
                if not self.minLight <= colony.get("redNight", 0) <= self.maxLight:
                    print(f"{RED}Error: Invalid red night value for {name}{NC}")
                    boundsFlag = True
                if not self.minLight <= colony.get("blueDay", 0) <= self.maxLight:
                    print(f"{RED}Error: Invalid blue day value for {name}{NC}")
                    boundsFlag = True
                if not self.minLight <= colony.get("blueNight", 0) <= self.maxLight:
                    print(f"{RED}Error: Invalid blue night value for {name}{NC}")
                    boundsFlag = True
                if not self.minDay <= colony.get("dayInterval", "01:00:00") <= self.maxDay:
                    print(f"{RED}Error: Invalid day interval for {name}{NC}")
                    boundsFlag = True
                if not self.minNight <= colony.get("nightInterval", "01:00:00") <= self.maxNight:
                    print(f"{RED}Error: Invalid night interval for {name}{NC}")
                    boundsFlag = True
                if boundsFlag:
                    print(f"{YELLOW}Please check the bounds for {name}{NC}")
                else:
                    print(f"{GREEN}No errors found for {name}{NC}")
                
            input("Press enter to continue...")
    
    # List colonies 
    def listColonies(self):
        print("List of active colonies:")
        sortedColonies = sorted(self.master.colonies.items(), key=lambda x: x[0])
        for colonyID, _ in sortedColonies:
            print(f'Colony{colonyID}')

    # Display main menu    
    def displayMainMenu(self):
        self.clearScreen()
        print("Main Menu")
        print("1. Insert colony")
        print("2. Extract colony")
        print("3. View images")
        print("4. Check colonies settings")
        print("5. Change colony settings")
        print("6. Change observation interval")
        print("7. Check bound settings")
        print("8. Observe colony (debug)")
        print("0. Exit")

    # Display colony settings
    def changeColonySettings(self, colonyID):
        colony = self.master.colonies.get(colonyID)
        if colony:
            newDayTemp = colony.dayTemp
            newNightTemp = colony.nightTemp
            newRedDay = colony.redDay
            newRedNight = colony.redNight
            newBlueDay = colony.blueDay
            newBlueNight = colony.blueNight
            newDayInterval = colony.dayInterval
            newNightInterval = colony.nightInterval

            print(f"Current settings for Colony{colonyID}:")
            print("1. Day Temperature:", newDayTemp)
            print("2. Night Temperature:", newNightTemp)
            print("3. Red Day:", newRedDay)
            print("4. Red Night:", newRedNight)
            print("5. Blue Day:", newBlueDay)
            print("6. Blue Night:", newBlueNight)
            print("7. Day Interval:", newDayInterval)
            print("8. Night Interval:", newNightInterval)
            print("0. Go back to main menu")

            while True:
                choice = input("Enter your choice (0. Go back): ")
                if choice == "0":
                    break
                elif choice == "1":
                    newDayTemp = int(input("Enter new Day Temperature: "))
                    if self.minTemp <= newDayTemp <= self.maxTemp:
                        newDayTemp = newDayTemp
                    else:
                        print("Invalid input!")
                        newDayTemp = colony.dayTemp
                elif choice == "2":
                    newNightTemp = int(input("Enter new Night Temperature: "))
                    if self.minTemp <= newNightTemp <= self.maxTemp:
                        newNightTemp = newNightTemp
                    else:
                        print("Invalid input!")
                        newNightTemp = colony.nightTemp
                elif choice == "3":
                    newRedDay = int(input("Enter new Red Day value: "))
                    if self.minLight <= newRedDay <= self.maxLight:
                        newRedDay = newRedDay
                    else:
                        print("Invalid input!")
                        newRedDay = colony.redDay
                elif choice == "4":
                    newRedNight = int(input("Enter new Red Night value: "))
                    if self.minLight <= newRedNight <= self.maxLight:
                        newRedNight = newRedNight
                    else:
                        print("Invalid input!")
                        newRedNight = colony.redNight
                elif choice == "5":
                    newBlueDay = int(input("Enter new Blue Day value: "))
                    if self.minLight <= newBlueDay <= self.maxLight:
                        newBlueDay = newBlueDay
                    else:
                        print("Invalid input!")
                        newBlueDay = colony.blueDay
                elif choice == "6":
                    newBlueNight = int(input("Enter new Blue Night value: "))
                    if self.minLight <= newBlueNight <= self.maxLight:
                        newBlueNight = newBlueNight
                    else:
                        print("Invalid input!")
                        newBlueNight = colony.blueNight
                elif choice == "7":
                    newDayInterval = datetime.strptime(input("Enter new Day Interval (HH:MM:SS): "),  "%H:%M:%S").time()
                    if self.minDay <= newDayInterval <= self.maxDay:
                        newDayInterval = newDayInterval
                    else:
                        print("Invalid input!")
                        newDayInterval = colony.dayInterval
                elif choice == "8":
                    newNightInterval = datetime.strptime(input("Enter new Night Interval (HH:MM:SS): "), "%H:%M:%S").time()
                    if self.minNight <= newNightInterval <= self.maxNight:
                        newNightInterval = newNightInterval
                    else:
                        print("Invalid input!")
                        newNightInterval = colony.nightInterval
                else:
                    print("Invalid input!")

            # After settings are changed, update the observation data
            self.master.setLights(colonyID, newRedDay, newRedNight, newBlueDay, newBlueNight)
            self.master.setTemperature(colonyID, newDayTemp, newNightTemp)
            self.master.setObservationInterval(colonyID, newDayInterval, newNightInterval)
            self.master.getObservationData(colonyID)

    # Update master with data from .json file
    def __updateMaster(self):
        # add values from .json file to master
        with open(JSON_PATH, 'r') as f:
            try:
                data = json.load(f)
                for colony_id, colony_data in data.items():
                    try:
                        colonyID = int(colony_data.get("id"))
                        startDate = datetime.strptime(colony_data.get("startDate"), "%Y-%m-%d").date()
                        lastObservation = datetime.strptime(colony_data.get("lastObservation"), "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")
                        dayTemp = int(colony_data.get("dayTemperature", 15))  # Default value: 15
                        nightTemp = int(colony_data.get("nightTemperature", 15))  # Default value: 15
                        redDay = int(colony_data.get("redDay", 0))  # Default value: 0
                        redNight = int(colony_data.get("redNight", 0))  # Default value: 0
                        blueDay = int(colony_data.get("blueDay", 0))  # Default value: 0
                        blueNight = int(colony_data.get("blueNight", 0))  # Default value: 0
                        dayInterval = colony_data.get("dayInterval", "01:00:00")  # Default value: 01:00:00
                        nightInterval = colony_data.get("nightInterval", "01:00:00")  # Default value: 01:00:00

                        self.master.insertColony(colonyID)
                        self.master.setTemperature(colonyID, dayTemp, nightTemp)
                        self.master.setLights(colonyID, redDay, redNight, blueDay, blueNight)
                        self.master.setObservationInterval(colonyID, dayInterval, nightInterval, startDate, lastObservation)
                        self.master.getObservationData(colonyID)
                        
                    except ValueError:
                        print(f"Error: Invalid colony ID for colony {colony_id}")
            except json.decoder.JSONDecodeError:
                print("Error: No data in colonyData.json")
                with open(JSON_PATH, 'w') as f:
                    json.dump({}, f)

    # Clear screen
    def clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')       
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

    # Show images
    def showImages(self, colonyID):
        self.clearScreen()

        colony_folder = f"colony{colonyID}"
        colony_path = os.path.join(IMAGE_PATH, colony_folder)

        if os.path.exists(colony_path) and os.path.isdir(colony_path):
            image_files = [image for image in os.listdir(colony_path) if image.endswith(('.jpg', '.png', '.jpeg'))]

            if image_files:
                # Sort the image files by modification time (most recent first)
                image_files.sort(key=lambda x: os.path.getmtime(os.path.join(colony_path, x)), reverse=True)
                most_recent_image = image_files[0]
                image_path = os.path.join(colony_path, most_recent_image)

                try:
                    os.system(f"eog {image_path} &")
                except Exception as e:
                    print(f"Error displaying image: {e}")
            else:
                print(f"No images found for colony{colonyID}.")
        else:
            print(f"Colony{colonyID} folder not found in {IMAGE_PATH}.")
                
            
if __name__ == "__main__":
    ui = UI()
    ui.run()