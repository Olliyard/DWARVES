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
    paramikoSSH = paramiko.SSHClient()
    paramikoSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramikoSSH.connect('', username='', password='') # IP, username, password
    paramikoSSH.exec_command('') # Path to executable on the Raspberry Pi
    self.__colonyImages[colonyID] = # Data from image folder

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
