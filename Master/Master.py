from datetime import datetime
from colony import Colony
import paramiko
import serial
import time
import json
import os

USB_PORT = "COM14" or "/dev/ttyUSB0"
RPI_ADDR = "192.168.0.104"
RPI_USERNAME = "rpi"
RPI_PASS = "raspberry"
RPI_PATH = "/home/pi/Documents/gitreps/DWARVES/RobotController/"
LOCAL_PATH = os.getcwd() + "/"
MAX_COLONIES = 10

class Master:
    def __init__(self, obsFreq=1):
        self.colonyStorage = {}
        self.observationFrequency = obsFreq
        self.ser = serial.Serial(USB_PORT, 9600, timeout=5)
        self.ssh = paramiko.SSHClient().set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    def __str__(self):
        colony_strings = [f"colony{i.id}" if i is not None else "Invalid Colony" for i in self.colonyStorage.values()]
        return f"Currently observing {len(self.colonyStorage)} colonies: {', '.join(colony_strings)}"

# COLONY HANDLING METHODS
    def checkColonies(self, colonyID):
        return colonyID in self.colonyStorage

    def getAvailability(self):
        if len(self.colonyStorage) == MAX_COLONIES:
            msg = "ERROR: No available space in system."
            self.logMessage(msg)
            return False
        else:
            return True

    def insertColony(self, colonyID):
        if 1 <= int(colonyID) <= MAX_COLONIES:
            if colonyID not in self.colonyStorage and self.getAvailability():
                newColony = Colony(colonyID, status=True)
                self.colonyStorage[colonyID] = newColony
                self.logMessage(f"Colony{colonyID}: Colony inserted into system.")
                return newColony
            else:
                print("ERROR: Colony already exists or no availability.")
                self.logMessage(f"ERROR: Colony{colonyID} could not be inserted into the system. Already exists or no availability.")
                return None
        else:
            print("ERROR: Invalid colony ID.")
            self.logMessage(f"ERROR: Invalid colony ID. Colony ID should be between 1 and {MAX_COLONIES}.")
            return None

    def extractColony(self, colonyID):
        if self.checkColonies(colonyID):
            extracted_colony = self.colonyStorage.pop(colonyID, None)
            if extracted_colony:
                # Remove the colony from colonyData.json
                filename = "filesys/colonyData.json"
                try:
                    with open(filename, "r") as file:
                        try:
                            all_colonies_data = json.load(file)
                        except json.JSONDecodeError:
                            all_colonies_data = {}
                except FileNotFoundError:
                    all_colonies_data = {}

                active_colony_ids = set(map(str, self.colonyStorage.keys()))
                filtered_colonies_data = {key: value for key, value in all_colonies_data.items() if key[6:] in active_colony_ids}

                with open(filename, "w") as file:
                    json.dump(filtered_colonies_data, file, indent=4)

                self.logMessage(f"Colony{colonyID}: Removed from system and {filename}.")
                return True
            else:
                self.logMessage(f"ERROR: Unable to remove Colony{colonyID} from system.")
                return False
        else:
            self.logMessage(f"ERROR: Colony{colonyID} does not exist in the system.")
            return False

# OBSERVATION METHODS
    def observeColony(self, colonyID, colony=None):
        time.sleep(2)
        self.ser.flushInput()
        self.ser.write(f"<get,{colonyID}>".encode("utf-8"))
        response = self.ser.readline().decode().strip()
        if response:
            values = response.split(",")
            if len(values) >= 3:
                temp = int(values[0]) if values[0] else 0
                red = int(values[1]) if values[1] else 0
                blue = int(values[2]) if values[2] else 0

                colony = self.updateColony(colonyID, colony, obsTemp=temp)
                if colony is not None:
                    self.logMessage(f"Colony{colony.id}: Observed values for temp: {temp}, red: {red}, blue: {blue}.")
        else:
            err = "ERROR: No response from Arduino"
            self.logMessage(err)

    def getObservationData(self, colonyID, colony=None):
        if not self.checkColonies(colonyID):
            self.logMessage(f"ERROR: Colony{colonyID} does not exist in the system (if not getObservationData).")
            return

        colony = self.updateColony(colonyID, colony)

        if colony is None:
            self.logMessage(f"ERROR: Colony{colonyID} does not exist in the system (getObservationData).")
            return

        filename = f"{LOCAL_PATH}filesys/colonyData.json"
        with open(filename, "r") as file:
            try:
                all_colonies_data = json.load(file)
            except json.JSONDecodeError:
                all_colonies_data = {}

        all_colonies_data[f"colony{colony.id}"] = {
            "id": int(colony.id),
            "occupied": colony.status,
            "daytime_hours": str(colony.dayInterval),
            "daytime_temperature": colony.dayTemp,
            "daytime_red_light": colony.redDay,
            "daytime_blue_light": colony.blueDay,
            "nighttime_hours": str(colony.nightInterval),
            "nighttime_temperature": colony.nightTemp,
            "nighttime_red_light": colony.redNight,
            "nighttime_blue_light": colony.blueNight,
            "observed_temperature": colony.obsTemp,
            "observation_interval": self.observationFrequency,
            "experiment_start_date": str(colony.startDate),
            "last_observation_date": str(colony.lastObsTime),
        }
        sorted_colonies_data = dict(
            sorted(all_colonies_data.items(), key=lambda x: int(x[1]["id"]))
        )

        with open(filename, "w") as file:
            json.dump(sorted_colonies_data, file, indent=4)

        self.logMessage(f"Colony{colony.id}: Colony successfully written to {filename}.")

# SET METHODS
    def setLight(self, colonyID, colony=None, redDay=0, blueDay=0, redNight=0, blueNight=0):
        colony = self.updateColony(colonyID, colony, redDay=redDay, blueDay=blueDay, redNight=redNight, blueNight=blueNight)
        if colony is not None:
            time.sleep(2)
            self.ser.flushInput()
            if colony.startTime <= datetime.now().time() <= colony.dayInterval:
                self.ser.write(f"<setl,{colony.id},{colony.redDay},{colony.blueDay}>".encode("utf-8"))
            else:
                self.ser.write(f"<setl,{colony.id},{colony.redNight},{colony.blueNight}>".encode("utf-8"))

    def setTemperature(self, colonyID, colony=None, dayTemp=0, nightTemp=0):
        colony = self.updateColony(colonyID, colony, dayTemp=dayTemp, nightTemp=nightTemp)
        if colony is not None:
            time.sleep(2)
            self.ser.flushInput()
            if colony.startTime <= datetime.now().time() <= colony.dayInterval:
                self.ser.write(f"<sett,{colony.id},{colony.nightTemp}>".encode("utf-8"))
            else:
                self.ser.write(f"<sett,{colony.id},{colony.nightTemp}>".encode("utf-8"))

    def setObservationInterval(self, colonyID, colony=None, dayInterval=0, nightInterval=0):
        dayInterval = datetime.strptime(f"{dayInterval}:00:00", "%H:%M:%S").time()
        nightInterval = datetime.strptime(f"{nightInterval}:00:00", "%H:%M:%S").time()
        colony = self.updateColony(colonyID, colony, dayInterval=dayInterval, nightInterval=nightInterval)
        if colony is not None:
            self.logMessage(f"Colony{colony.id}: Updated observation interval to day: {colony.dayInterval}, night: {colony.nightInterval}")

    def setObservationFrequency(self, freq):
        self.observationFrequency = freq
        self.logMessage(f"ALL COLONIES: Observation frequency set to {freq} minutes.")

# INTERNAL METHODS
    def logMessage(self, msg):
        with open(f'{LOCAL_PATH}filesys/logfile.txt', 'a') as file:
            file.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M")}: {msg}\n')

    def printColonies(self, colonyID=None):
        if colonyID is not None:
            colony_instance = self.colonyStorage.get(colonyID)
            if colony_instance is not None:
                print(colony_instance)
        else:
            for colonyID, colony_instance in self.colonyStorage.items():
                print(colony_instance)

    def updateColony(self, colonyID=1, colony=None, file=False, **attributeUpdates):
        if file:
            if not self.checkColonies(colonyID):
                new_colony = self.insertColony(colonyID)
                if new_colony is not None:
                    self.logMessage(f"Colony{colonyID}: Updated settings from settings.json")
                    return new_colony
                else:
                    return None

            updated_colony = self.colonyStorage[colonyID]
            updated_colony.updateAttributesFromFile(f'{LOCAL_PATH}filesys/settings.json')

            with open(f'{LOCAL_PATH}filesys/settings.json', 'r') as f:
                settings = json.load(f)
                settings = settings.get(f'colony{colonyID}', {})
                if settings:
                    self.observationFrequency = settings.get('observation_interval', self.observationFrequency)
                    self.logMessage(f"Colony{colonyID}: Updated settings from settings.json")
                    return updated_colony
                else:
                    self.logMessage(f"ERROR: Colony{colonyID} settings not found in settings.json")
                    return None
                
        elif self.checkColonies(colonyID):
            existing_colony = self.colonyStorage[colonyID]
            existing_colony.update(attributeUpdates)
            return existing_colony
        else:
            self.logMessage(f"ERROR: Colony{colonyID} does not exist in the system.")
            return None

# Create an instance of the Master class
# master = Master(1)

# print("Adding colony 1:")               # TEST PASSED
# colony1 = master.insertColony(1)
# master.printColonies(1)

# print("Default settings:")              # TEST PASSED
# master.getObservationData(colony1.id)
# time.sleep(2)                           # BEFORE UPDATE

# print("Updating settings:")             # TEST PASSED
# master.setLight(colony1.id, redDay=100, blueDay=100, redNight=10, blueNight=10)
# master.setTemperature(colony1.id, dayTemp=25, nightTemp=20)
# master.setObservationInterval(colony1.id, dayInterval=12, nightInterval=12)
# master.observeColony(colony1.id)
# master.getObservationData(colony1.id)
# time.sleep(2)                           # BEFORE UPDATE

# print("Updating settings from file:")   # TEST PASSED
# master.updateColony(colony1.id, file=True)
# master.getObservationData(colony1.id)

# print("Adding colony 2:")               # TEST PASSED
# colony2 = master.insertColony(2)
# master.getObservationData(colony2.id)

# print("Adding colony 3 from file:")     # TEST PASSED
# colony3 = master.insertColony(3)
# master.updateColony(colony3.id, colony3, file=True)
# master.getObservationData(colony3.id)

# print(master)
