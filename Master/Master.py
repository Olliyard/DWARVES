from datetime import datetime
from colony import Colony
import threading
import paramiko
import serial
import time
import json
import os

USB_PORT = "COM14" # "/dev/ttyUSB0"
RPI_ADDR = "192.168.30.231"
RPI_USERNAME = "rpi"
RPI_PASS = "raspberry"
RPI_PATH = "/home/pi/DWARVES/RobotController"
LOGFILE_PATH = os.path.join(os.getcwd(), "filesys", "logfile.txt")
JSON_PATH = os.path.join(os.getcwd(), "filesys", "colonyData.json")
IMAGE_PATH = os.path.join(os.getcwd(), "images")
LOCAL_PATH = os.getcwd()
MAX_COLONIES = 10
DELAY = 2

class Master:
    def __init__(self):
        self.colonies = {}
        self.observationFrequency = 1
        self.observe_timer = None
        self.serial = serial.Serial(USB_PORT, 9600, timeout=5)

    # String representation of Master
    def __str__(self):
        return f"Colonies: {self.colonies}\n"

    # insert colony
    def insertColony(self, colonyID):
        if self.getAvailability() and not self.checkColony(colonyID) and self.checkLoadingZone():            
            # Move colony to position
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(RPI_ADDR, username=RPI_USERNAME, password=RPI_PASS)

                # Trigger robot movement on the Raspberry Pi
                cmd = f'python3 {RPI_PATH}/Motor/motorControl.py {colonyID} {colonyID} "down"'
                _, stdout, stderr = ssh.exec_command(cmd)

                # Wait for the command to complete
                exit_status = stdout.channel.recv_exit_status()
                if exit_status == 0:
                    self.__logMessage(f"Colony{colonyID}", stdout.read().decode('utf-8'))
                    self.__logMessage(f"Colony{colonyID}", stderr.read().decode('utf-8'))
                    print(f"Robot moved to colony {colonyID}.")

            except Exception as e:
                print(f"Error: {str(e)}")

            finally:
                # Close the connection
                ssh.close()
            
            self.colonies[colonyID] = Colony(colonyID)  # create colony object
            self.__logMessage(f"Colony{colonyID}", "Inserted.")
            
        else:
            self.__logMessage("ERROR", f"Colony{colonyID} could not be inserted.")
  
    # extract colony  
    def extractColony(self, colonyID):
        if self.checkColony(colonyID) and self.checkLoadingZone():
            # Move robot to colony
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(RPI_ADDR, username=RPI_USERNAME, password=RPI_PASS)

                # Trigger robot movement on the Raspberry Pi
                cmd = f'python3 {RPI_PATH}/Motor/motorControl.py {colonyID} {colonyID} "up"'
                _, stdout, stderr = ssh.exec_command(cmd)

                # Wait for the command to complete
                exit_status = stdout.channel.recv_exit_status()
                if exit_status == 0:
                    self.__logMessage(f"Colony{colonyID}", stdout.read().decode('utf-8'))
                    self.__logMessage(f"Colony{colonyID}", stderr.read().decode('utf-8'))
                    print(f"Robot moved to colony {colonyID}.")

            except Exception as e:
                print(f"Error: {str(e)}")

            finally:
                # Close the connection
                ssh.close()
            
            
            self.colonies.pop(colonyID)
            self.__logMessage(f"Colony{colonyID}", "Extracted.")
            return True
        else:
            self.__logMessage("ERROR", f"Colony{colonyID} could not be extracted.")
            return False
    
    # check loading zone
    def checkLoadingZone(self):
        time.sleep(DELAY)
        self.serial.flushInput()
        self.serial.write(f"<lz>".encode("utf-8"))
        self.serial.readline()
        status = self.serial.readline().decode().strip()[7:]
        if status == "1":
            # print("Loading zone occupied.")
            self.__logMessage("Master", "Loading zone occupied.")
            return False
        else:
            # print("Loading zone free.")
            self.__logMessage("Master", "Loading zone free.")
            return True
    
    # get colony data
    def observeColony(self, colonyID):
        # connect to arduino, get temperature and note it.
        # also note time of observation
        if self.checkColony(colonyID):
            time.sleep(DELAY)
            self.serial.flushInput()
            self.serial.write(f"<get,{colonyID}>".encode("utf-8"))
            self.serial.readline()
            self.colonies[colonyID].obsTemp = float(self.serial.readline().decode().strip()[7:])
            self.colonies[colonyID].lastObsTime = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # Connect to RPi, get image
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(RPI_ADDR, username=RPI_USERNAME, password=RPI_PASS)

                # Trigger image capture and processing on the Raspberry Pi
                cmd = f'python3 {RPI_PATH}/Camera/captureImage.py {colonyID}'
                _, stdout, _ = ssh.exec_command(cmd)

                # Wait for the command to complete
                exit_status = stdout.channel.recv_exit_status()

                if exit_status == 0:
                    # Receive data from the Raspberry Pi
                    remote_path = f'{RPI_PATH}/Camera/colony{colonyID}/'
                    local_path = f'{IMAGE_PATH}/colony{colonyID}/'

                    # Create a local directory if it doesn't exist
                    os.makedirs(local_path, exist_ok=True)

                    # List files in the folder
                    image_files = [file for file in os.listdir(remote_path) if file.endswith(('.jpg', '.txt', '.png'))]
                    self.__logMessage(f"Colony{colonyID}", f"Files found: {image_files}")

                    # Loop through the files and receive them
                    for file in image_files:
                        try:
                            src_path = os.path.join(remote_path, file)
                            dest_path = os.path.join(local_path, file)
                            ssh.scp.get(src_path, dest_path)
                            # print(f"Extracting {file}...")

                        except Exception as e:
                            self.__logMessage(f"ERROR", f"Error extracting {file}: {str(e)}")

                    # Remove folders on the Raspberry Pi
                    cmd = f'rm -rf {remote_path}'
                    _, stdout, _ = ssh.exec_command(cmd)

                    # Wait for the command to complete
                    exit_status = stdout.channel.recv_exit_status()
                    
                    if exit_status == 0:
                        self.__logMessage(f"Colony{colonyID}", f"Extracted images.")

            except Exception as e:
                print(f"Error: {str(e)}")

            finally:
                # Close the connection
                ssh.close()
            
            self.__logMessage(f"Colony{colonyID}", f"Observed at {self.colonies[colonyID].lastObsTime}.")
            return True
        else:
            # print(f"Colony {colonyID} not observed.")
            self.__logMessage(f"ERROR", f"Colony{colonyID} could not be observed.")
            return False

    # set colony lights
    def setLights(self, colonyID, redDay, redNight, blueDay, blueNight):
        # connect to arduino, set lights
        if self.checkColony(colonyID):
            time.sleep(DELAY)
            self.serial.flushInput()
            # if interval is between start and dayInterval, set day lights
            if self.__checkTime(colonyID): # if day
                self.serial.write(f"<setl,{colonyID},{redDay},{blueDay}>".encode("utf-8"))

            
            else:  # else set night lights
                self.serial.write(f"<setl,{colonyID},{redNight},{blueNight}>".encode("utf-8"))

            # Update colony lights for JSON
            self.colonies[colonyID].redDay = redDay
            self.colonies[colonyID].blueDay = blueDay
            self.colonies[colonyID].redNight = redNight
            self.colonies[colonyID].blueNight = blueNight

            # print(f"Colony {colonyID} lights set.")
            self.__logMessage(f"Colony{colonyID}", f"Set lights to R:{redDay}/{redNight} B:{blueDay}/{blueNight}.")
            return True
        else:
            # print(f"Colony {colonyID} lights not set.")
            self.__logMessage("ERROR", f"Colony{colonyID} lights not set.")
            return False

    # set colony temperature
    def setTemperature(self, colonyID, dayTemp, nightTemp):
        # connect to arduino, set temperature
        if self.checkColony(colonyID):
            time.sleep(DELAY)
            self.serial.flushInput()
            if self.__checkTime(colonyID): # if day
                self.serial.write(f"<sett,{colonyID},{dayTemp}>".encode("utf-8"))
                
            else:  # else set night temperature
                self.serial.write(f"<sett,{colonyID},{nightTemp}>".encode("utf-8"))

            # Update colony temperature for JSON
            self.colonies[colonyID].dayTemp = dayTemp
            self.colonies[colonyID].nightTemp = nightTemp
                
            # print(f"Colony {colonyID} temperature set.")
            self.__logMessage(f"Colony{colonyID}", f"Set temperature to {dayTemp}/{nightTemp}.")
            return True
        else:
            # print(f"Colony {colonyID} temperature not set.")
            self.__logMessage("ERROR", f"Colony{colonyID} temperature not set.")
            return False

    # set observation interval
    def setObservationInterval(self, colonyID, dayInterval, nightInterval, startDate=None, lastObservation=None):
        if self.checkColony(colonyID):
            self.colonies[colonyID].dayInterval = dayInterval
            self.colonies[colonyID].nightInterval = nightInterval
            
            if startDate:
                self.colonies[colonyID].startDate = startDate
                
            if lastObservation:
                self.colonies[colonyID].lastObsTime = lastObservation
                    
            # print(f"Colony {colonyID} observation interval set.")
            self.__logMessage(f"Colony{colonyID}", f"Set observation interval to {dayInterval}/{nightInterval}.")
            return True
        else:
            # print(f"Colony {colonyID} observation interval not set.")
            self.__logMessage("ERROR", f"Colony{colonyID} observation interval not set.")
            return False

    # set observation frequency
    def setObservationFrequency(self, observationFrequency):
        self.observationFrequency = observationFrequency
        # print(f"Observation frequency set to {observationFrequency} hours.")
        self.__logMessage("Master", f"Set observation frequency to {observationFrequency} hours.")

    # write colony data to JSON file
    def getObservationData(self, colonyID):
        with open(JSON_PATH, "r") as f:
            try:
                allColoniesData = json.load(f)
            except json.decoder.JSONDecodeError:
                allColoniesData = {}
            
        colonyData = self.__setValues(colonyID)
        
        if colonyData:
            allColoniesData[f'colony{colonyID}'] = colonyData
            # print(f"Colony {colonyID} data: {colonyData}")
            self.__logMessage("colonyData.json", f"Updating colony{colonyID} data.")
        elif f'colony{colonyID}' in allColoniesData:
            del allColoniesData[f'colony{colonyID}'] # delete data if colony doesn't exist
            self.__logMessage("colonyData.json", f"Deleted colony{colonyID} data.")
        else:
            # print(f"Colony {colonyID} not found.")
            self.__logMessage("ERROR", f"Colony{colonyID} not found.")
            return False
            
        sortedColonies = dict(sorted(allColoniesData.items(), key=lambda x: int(x[0][6:])))
        with open(JSON_PATH, "w") as f:
            json.dump(sortedColonies, f, indent=4)
    
    # check if colony exists
    def checkColony(self, colonyID):
        if colonyID in self.colonies:
            # print(f"Colony {colonyID} found.")
            return True
        else:
            # print(f"Colony {colonyID} not found.")
            return False
       
    # check if there is space for a colony 
    def getAvailability(self):
        if len(self.colonies) < MAX_COLONIES:
            # print(f"Available space: {MAX_COLONIES - len(self.colonies)}")
            return MAX_COLONIES - len(self.colonies)
        else:
            # print("No available space in system.")
            return False
        
    # private method to set values for colony data
    def __setValues(self, colonyID):
        colony = self.colonies.get(colonyID)
        if colony:  # if colony exists
            colonyData = {
                "id": int(colony.id),
                "startDate": str(colony.startDate),
                "lastObservation": str(colony.lastObsTime),
                "observedTemperature": colony.obsTemp,
                "dayTemperature": colony.dayTemp,
                "nightTemperature": colony.nightTemp,
                "redDay": colony.redDay,
                "redNight": colony.redNight,
                "blueDay": colony.blueDay,
                "blueNight": colony.blueNight,
                "dayInterval": str(colony.dayInterval),
                "nightInterval": str(colony.nightInterval),
            }
        else:    # if colony doesn't exist
            colonyData = {}
        return colonyData
    
        # check if colony exists

    # private method to check if it's day or night   
    def __checkTime(self, colonyID):
        startTime = str(self.colonies[colonyID].startTime)
        currentTime = str(datetime.now().time())
        dayInterval = str(self.colonies[colonyID].dayInterval)
        nightInterval = str(self.colonies[colonyID].nightInterval)

        if startTime <= currentTime <= dayInterval:
            return True
        elif dayInterval <= currentTime <= nightInterval:
            return False
    
    # private method to log messages
    def __logMessage(self, prefix, message):
        with open(LOGFILE_PATH, "a") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {prefix}: {message}\n")

    # Start the observation scheduler
    def startObservationScheduler(self):
        self.scheduleObservation()

    # Schedule the next observation
    def scheduleObservation(self):
        self.observe_timer = threading.Timer(self.observationFrequency * 3600, self.observeColony)
        self.observe_timer.start()

    # Stop the observation scheduler
    def stopObservationScheduler(self):
        if self.observe_timer:
            self.observe_timer.cancel()


# master = Master()

# # Test 1: insert colony
# master.insertColony(1)
# master.getObservationData(1)

# # Test 2: extract colony
# master.extractColony(1)
# master.getObservationData(1)

# # Test 3: insert colony twice
# master.insertColony(1)
# master.insertColony(1)
# master.getObservationData(1)

# # Test 4: set lights
# master.setLights(1, 90, 80, 20, 10)
# master.getObservationData(1)

# # Test 5: set temperature
# master.setTemperature(1, 30, 20)
# master.getObservationData(1)

# # Test 6: set observation interval
# master.setObservationInterval(1, "10:00:00", "14:00:00")
# master.getObservationData(1)

# # Test 7: set observation frequency
# master.setObservationFrequency(2)
# master.getObservationData(1)

# # Test 8: observe colony
# master.observeColony(1)
# master.getObservationData(1)

# # Test 9: get observation data
# master.getObservationData(1)

# # Test 9: check colony
# print(master.checkColony(1))

# # Test 10: get availability
# print("Available spaces:", master.getAvailability())

# # Test 11: Insert 10 colonies
# for i in range(1, 11):
#     master.insertColony(i)
#     master.getObservationData(i)

# # Test 12: Insert 11th colony
# master.insertColony(11)
# master.getObservationData(11)