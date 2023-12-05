import paramiko
import time
import os
import sys
import serial

class Master:
    def __init__(self):
        self.__colonyStorage = {}
        self.__colonyImages = {}
        self.__colonyMeasurement = {}
        self.__dayInterval = 12
        self.__nightInterval = 12
        self.__observationFrequency = 1
        self.__setColonyRed = 0
        self.__setColonyBlue = 0
        self.__colonyDayTemp = 0
        self.__colonyNightTemp = 0
    
    def checkColonies(self, colonyID):
        if colonyID in self.__colonyStorage:
            return True
        else:
            return False
    
    def getAvailability(self):
        if len(self.__colonyStorage) == 0:
            return False
        else:
            return True
    
    def checkLoadingZone():
        paramikoSSH = paramiko.SSHClient()
        paramikoSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        paramikoSSH.connect('', username='', password='') # IP, username, password
        paramikoSSH.exec_command('') # Path to executable on the Raspberry Pi
        
        pass

    def insertColony(self, colonyID):
        if colonyID not in self.__colonyStorage:
            paramikoSSH = paramiko.SSHClient()
            paramikoSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            paramikoSSH.connect('', username='', password='') # IP, username, password
            paramikoSSH.exec_command('') # Path to executable on the Raspberry Pi
            # If succesful, add colonyID to colonyStorage
            self.__colonyStorage.append(colonyID)
        else:
            return 0
    
def extractColony(self, colonyID):
    if colonyID in self.colonyStorage:
        paramikoSSH = paramiko.SSHClient()
        paramikoSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        paramikoSSH.connect('', username='', password='') # IP, username, password
        paramikoSSH.exec_command('') # Path to executable on the Raspberry Pi
        # If succesful, remove colonyID from colonyStorage
        self.__colonyStorage.remove(colonyID)
    else:
        return 0
    
def getObservationData(self, colonyID):
    # Call a method from Arduino to get data
    self.__colonyMeasurement[colonyID] = # Data from Arduino
    pass

def getObservationFootage(self, colonyID):
    # Create a connection to the Raspberry Pi
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.0.123', username='pi', password='raspberry')

    # Trigger image capture and processing on the Raspberry Pi
    stdin, stdout, stderr = ssh.exec_command(f'python3 /home/pi/Documents/gitreps/DWARVES/RobotController/Camera/captureImage.py {colonyID}')
    # Wait for the command to complete
    exit_status = stdout.channel.recv_exit_status()

    if exit_status == 0:
        # Receive data from the Raspberry Pi
        sftp = ssh.open_sftp()
        print(f'Locating colony{colonyID} images files...')
        
        # List files in the folder
        image_files = [file for file in sftp.listdir(f'/home/pi/Documents/gitreps/DWARVES/RobotController/Camera/colony{colonyID}/') if file.endswith(('.jpg', '.txt', '.png'))]
        print(f'Files found: {image_files}')

        # Loop through the files and receive them
        for file in image_files:
            remote_path = f'/home/pi/Documents/gitreps/DWARVES/RobotController/Camera/colony{colonyID}'
            local_path = f'/home/stud/Documents/gitreps/DWARVES/Master/colony{colonyID}'

            # Make local dir if none
            os.makedirs(local_path, exist_ok=True)
            try:
                sftp.get(f'{remote_path}/{file}', f'{local_path}/{file}')
                print("Extracting images...")
            
            except Exception as e:
                print(f"Error extracting images: {str(e)}")

        print(f'Image data for colony{colonyID} successfully extracted to {local_path}.')
        
        # Remove folders on the Raspberry Pi
        stdin, stdout, stderr = ssh.exec_command(f'rm -rf {remote_path}')

        # Wait for the command to complete
        exit_status = stdout.channel.recv_exit_status()

        # Close the connection
        sftp.close()
        ssh.close()
        
        self.__colonyImages[colonyID] = local_path

    else:
        # If the command was not successful, handle the error as needed
        print(f"Error: {stderr.read().decode('utf-8')}")
        ssh.close()
        return None

def saveObservationData(colonyID):
    # Save data to local storage
    pass

def saveObservationFootage(colonyID):
    # Save footage to local storage
    pass

def deleteObservationData(colonyID):
    # Delete data from local storage
    pass

def deleteObservationFootage(colonyID):
    # Delete footage from local storage
    pass

def setTemperature(colonyID, colonyDayTemp, colonyNightTemp):
    # Call a method from Arduino to set temperature
    pass

def setLight(colonyID, setColonyRed, setColonyBlue):
    # Call a method from Arduino to set light
    pass

def setObservationInterval(colonyID, dayInterval, nightInterval):
    _dayInterval = dayInterval
    _nightInterval = nightInterval
    pass

def setObservationFrequency(colonyID, observationFrequency):
    _observationFrequency = observationFrequency
    pass

def pauseObservation(colonyID):
    # Call a method from Pi to pause observation
    pass

def logMessage(msg):
    # Log message to log file
    pass
