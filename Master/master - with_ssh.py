from datetime import datetime, time
from colony import Colony
import paramiko
import serial
import time
import json
import os

# USB_PORT = "/dev/ttyUSB0"  # Arduino Uno WiFi Rev2 (can be ttyUSB0)
USB_PORT = "COM14" or "/dev/ttyUSB0"
RPI_ADDR = "192.168.0.104"
RPI_USERNAME = "rpi"
RPI_PASS = "raspberry"
RPI_PATH = "/home/pi/Documents/gitreps/DWARVES/RobotController/"
LOCAL_PATH = os.getcwd() + "/"
MAX_COLONIES = 10

class Master:
    def __init__(self, obsFreq):
        self.colonyStorage = {}  # {colonyID: colonyInstance}
        self.observationFrequency = obsFreq
        self.ser = serial.Serial(USB_PORT, 9600, timeout=5)
        self.ssh = paramiko.SSHClient().set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    def __str__(self):
        return f"Currently observing {len(self.colonyStorage)} colonies: " + \
            ', '.join(f"colony{i.id}" for i in self.colonyStorage.values())

# Checking colonies and inserting/extracting
    def checkColonies(self, colonyID):
        if colonyID in self.colonyStorage:
            return True
        else:
            return False

    def getAvailability(self):
        if len(self.colonyStorage) == MAX_COLONIES:
            msg="ERROR: No available space in system."
            print(msg)
            self.logMessage(msg)
            return False
        else:
            return True

    def insertColony(self, colonyID):
        if self.checkColonies(colonyID) == False and self.getAvailability() == True:
            newColony = Colony(colonyID, status=True)
            self.colonyStorage[colonyID] = newColony
            self.logMessage(f"Colony{colonyID}: Colony inserted into system.")
            return newColony

    def extractColony(self, colonyID):
        if self.checkColonies(colonyID) == True:
            instance = self.colonyStorage[colonyID]
            instance.status = False
            self.logMessage(f"Colony{colonyID}: Colony removed from system.")
            del instance
            return True

# Observing colonies
    def observeColony(self, colonyID):
        # Wait for Arduino to initialize, flush input buffer, send a get command and read response from Arduino
        time.sleep(2)
        self.ser.flushInput()
        self.ser.write(f"<get,{colonyID}>".encode("utf-8"))  # Encode the string to bytes
        response = self.ser.readline().decode().strip()  # Decode the bytes to string
        if response:
            # print(f"Received response for get command: {response}") # debug
            values = response.split(",")  # Split the string into a list of strings
            if len(values) >= 3:
                temp = int(values[0]) if values[0] else 0
                red = int(values[1]) if values[1] else 0
                blue = int(values[2]) if values[2] else 0

                # debug
                # print(f'Set Temperature: {temp}')
                # print(f'Red Brightness: {red}')
                # print(f'Blue Brightness: {blue}')
                self.logMessage(f"Colony{colonyID}: Observed values for temp: {temp}, red: {red}, blue: {blue}.")             
            else:
                print("ERROR: Insufficient values in the response")
        else:
            err = "ERROR: No response from Arduino"
            print(err)
            self.logMessage(err)
                
        # Create a connection to the Raspberry Pi
        self.ssh.connect(RPI_ADDR, username=RPI_USERNAME, password=RPI_PASS)
        # Trigger image capture and processing on the Raspberry Pi
        _, stdout, stderr = self.ssh.exec_command(f'python3 {RPI_PATH}captureImage.py {colonyID}')
        if stdout.channel.recv_exit_status() == 0:
            sftp = self.ssh.open_sftp()
            image_files = [file for file in sftp.listdir(f'{RPI_PATH}colony{colonyID}/') if file.endswith(('.jpg', '.txt', '.png'))]
            # Loop through the files and receive them
            for file in image_files:
                # Make local dir if none
                os.makedirs(f'{LOCAL_PATH}/colony{colonyID}', exist_ok=True)
                try:
                    sftp.get(f'{RPI_PATH}colony{colonyID}/{file}', f'{LOCAL_PATH}colony{colonyID}/{file}')
                except Exception as e:
                    print(f"Error extracting images: {str(e)}")
                finally:
                    _, stdout, _ = self.ssh.exec_command(f'rm -rf {RPI_PATH}colony{colonyID}')
                    if stdout.channel.recv_exit_status() == 0:
                        self.logMessage(f"Colony{colonyID}: Image data successfully extracted to {LOCAL_PATH}colony{colonyID}.")

    def getObservationData(self, colony):
        # Write the colony instance to a json file
        self.updateColony(colony.id, colony)
        colonyInstance = self.colonyStorage.get(colony.id)
        if colonyInstance is not None:
            # Load existing data from the file
            with open(f"{LOCAL_PATH}filesys/colonyData.json", "a+") as file:
                file.seek(0)
                try:
                    all_colonies_data = json.load(file)
                except json.JSONDecodeError:
                    all_colonies_data = {}

                # Update the data
                all_colonies_data[f"colony{colonyInstance.id}"] = {
                    "id": colonyInstance.id,
                    "occupied": colonyInstance.status,
                    "daytime_hours": str(colonyInstance.dayInterval),
                    "daytime_temperature": colonyInstance.dayTemp,
                    "daytime_red_light": colonyInstance.redDay,
                    "daytime_blue_light": colonyInstance.blueDay,
                    "nighttime_hours": str(colonyInstance.nightInterval),
                    "nighttime_temperature": colonyInstance.nightTemp,
                    "nighttime_red_light": colonyInstance.redNight,
                    "nighttime_blue_light": colonyInstance.blueNight,
                    "observed_temperature": colonyInstance.obsTemp,
                    "observation_interval": self.observationFrequency,
                    "experiment_start_date": str(colonyInstance.startDate),
                    "last_observation_date": str(colonyInstance.lastObsTime),
                }
                sorted_colonies_data = dict(
                    sorted(all_colonies_data.items(), key=lambda x: int(x[1]["id"]))
                )
                # Write the updated data to the file
                with open(f"{LOCAL_PATH}filesys/colonyData.json", "w") as file:
                    json.dump(sorted_colonies_data, file, indent=4)
        
            self.logMessage(f"Colony{colony.id}: Colony successfully written to colonyData.json")
            
        else:
            err = f"ERROR: Colony{colony.id} does not exist in the system."
            print(err)
            self.logMessage(err)

# Change settings
    def setLight(self, colony, redDay=0, blueDay=0, redNight=0, blueNight=0):
        colony.redDay = redDay
        colony.blueDay = blueDay
        colony.redNight = redNight
        colony.blueNight = blueNight
        self.updateColony(colony.id, colony)
        # Create serial connection to Arduino COM14 port and send command <set,colonyID,red,blue>
        # Send a set command
        time.sleep(2)  # Wait for Arduino to initialize
        self.ser.flushInput()
        if colony.startTime <= datetime.now().time() <= colony.dayInterval:
            self.ser.write(f"<setl,{colony.id},{colony.redDay},{colony.blueDay}>".encode("utf-8"))
            response = self.ser.readline().decode().strip()
            if response:
                # print(f"Received response for set command: {response}") # debug
                self.logMessage(f"Colony{colony.id}: Set day lights to {colony.redDay} and {colony.blueDay}")
            else:
                err = "ERROR: No response from Arduino"
                print(err)
                self.logMessage(err)

        else:
            self.ser.write(f"<setl,{colony.id},{colony.redNight},{colony.blueNight}>".encode("utf-8"))
            response = self.ser.readline().decode().strip()
            if response:
                # print(f"Received response for set command: {response}") # debug
                self.logMessage(f"Colony{colony.id}: Set night lights to {colony.redNight} and {colony.blueNight}")
            else:
                err = "ERROR: No response from Arduino"
                print(err)
                self.logMessage(err)

    def setTemperature(self, colony, dayTemp, nightTemp):
        colony.dayTemp = dayTemp
        colony.nightTemp = nightTemp
        self.updateColony(colony.id, colony)
        # Create serial connection to Arduino COM14 port and send command <set,colonyID,red,blue>
        # Send a set command
        time.sleep(2)
        self.ser.flushInput()
        if colony.startTime <= datetime.now().time() <= colony.dayInterval:
            self.ser.write(f"<sett,{colony.id},{colony.dayTemp}>".encode("utf-8"))
            response = self.ser.readline().decode().strip()
            if response:
                # print(f"Received response for set command: {response}") # debug
                self.logMessage(f"Colony{colony.id}: Set day temperature to {colony.dayTemp}")
            else:
                err = "ERROR: No response from Arduino"
                print(err)
                self.logMessage(err)
                
        else:
            self.ser.write(f"<sett,{colony.id},{colony.nightTemp}>".encode("utf-8"))
            response = self.ser.readline().decode().strip()
            if response:
                # print(f"Received response for set command: {response}") # debug
                self.logMessage(f"Colony{colony.id}: Set night temperature to {colony.nightTemp}")
            else:
                err = "ERROR: No response from Arduino"
                print(err)
                self.logMessage(err)

    def setObservationInterval(self, colony, dayInterval, nightInterval):
        colony.dayInterval = dayInterval
        colony.nightInterval = nightInterval
        self.updateColony(colony.id, colony)
        self.logMessage(f"Colony{colony.id}: Updated observation interval to day: {dayInterval}, night: {nightInterval}")

    def setObservationFrequency(self, freq):
        self.observationFrequency = freq
        self.logMessage(f"ALL COLONIES: Observation frequency set to {freq} minutes.")

# Internal methods
    def logMessage(self, msg):
        # log messages in logfile
        with open(f'{LOCAL_PATH}filesys/logfile.txt', 'a') as file:
            file.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M")}: {msg}\n')

    def printColonies(self, colonyID=None):
        if colonyID is not None:
            colony_instance = self.colonyStorage.get(colonyID)
            if colony_instance is not None:
                print(colony_instance)
            else:
                print(f"Colony {colonyID} - status: Not Occupied")
        else:
            for colony_instance in self.colonyStorage.items():
                print(colony_instance)

    def updateColony(self, colonyID, colony, file=False):
        if self.checkColonies(colonyID) == True and file == False:
            self.colonyStorage[colonyID] = colony
        else:
            # Get values from UI settings file
            colony = self.colonyStorage[colonyID]
            colony.updateAttributesFromFile(f'{LOCAL_PATH}filesys/settings.json')
            
            with open(f'{LOCAL_PATH}filesys/settings.json', 'r') as f:
                settings = json.load(f)
                settings = settings.get(f'colony{colonyID}', {})
                if settings is not None:
                    self.observationFrequency = settings.get('observation_interval', self.observationFrequency)
                    self.logMessage(f"Colony{colonyID}: Updated settings from settings.json")

master = Master(1)

print("Adding colony 1:")
colony1 = master.insertColony(1)
master.printColonies(1)

print("Changing colony lights:")
colony1.blueDay = 50
colony1.redDay = 40
colony1.blueNight = 20
colony1.redNight = 10
master.setLight(colony1)                    # Ignores previous values set for instance.
master.setLight(colony1, 90, 80, 20, 10)    # Passes arguments correctly
master.observeColony(colony1.id)

print("Changing colony temperature:")
master.setTemperature(colony1, 30, 15)      # Same as previous
master.observeColony(colony1.id)
master.getObservationData(colony1)

print("Adding colony 2:")
colony2 = master.insertColony(2)
master.getObservationData(colony2)          # Default

print("Adding colony 3 from file:")
colony3 = master.insertColony(3)
master.updateColony(colony3.id, colony3, file=True)
master.getObservationData(colony3)          # Same as settings file

print(master)