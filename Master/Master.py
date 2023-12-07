import paramiko
from datetime import datetime, time, timedelta
import json
import os
import serial
from colony import Colony

USB_PORT = "/dev/ttyACM0"  # Arduino Uno WiFi Rev2 (can be ttyUSB0)
RPI_ADDR = '192.168.0.104'
RPI_USERNAME = 'rpi'
RPI_PASS = 'raspberry'
RPI_PATH = '/home/pi/Documents/gitreps/DWARVES/RobotController/'
LOCAL_PATH = os.getcwd() + '/'
MAX_COLONIES = 10

class Master:
    def __init__(self, observationFrequency=0):
        # List of colonies
        self.colonyStorage = {} # {colonyID: {colonyInstance: colonyInstance}}
        self.observationFrequency = observationFrequency


    '''Establishes an SSH connection to the Raspberry Pi and returns the connection object
    paramikoSSH: SSH connection object
    '''
    def _establish_ssh_connection(self):
        try:
            paramikoSSH = paramiko.SSHClient()
            paramikoSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            paramikoSSH.connect(RPI_ADDR, username=RPI_USERNAME, password=RPI_PASS)  # IP, username, password
            return paramikoSSH
        except Exception as e:
            print(f'Error: {e}')
            self.logMessage(f'Error: {e}')


    '''Establishes a serial connection to the Arduino and returns the connection object
    usb: Serial connection object
    '''
    def _establish_serial_connection(self):
        try:
            usb = serial.Serial(USB_PORT, 9600, timeout=2)
            return usb
        except Exception as e:
            print(f"Error: {e}")
            self.logMessage(f'Error: {e}')


    '''Adds a colony to the colonyStorage dictionary
    colonyID: ID of the colony to be added
    measurement_data: Dictionary containing the measurement data
    '''
    def _add_colony_measurement(self, colonyID, measurement_data):
        self.colonyStorage.setdefault(colonyID, {}).setdefault(measurement_data, []).append(measurement_data)
    
    
    '''Adds a colony to the colonyStorage dictionary
    colonyID: ID of the colony to be added
    image_data: Dictionary containing the image data
    '''
    def _add_colony_images(self, colonyID, image_data):
        self.colonyStorage.setdefault(colonyID, {}).setdefault(image_data, []).append(image_data)


    '''Returns the colonyStorage dictionary
    '''
    def checkColonies(self, colonyID):
        if colonyID in self.colonyStorage:
            print(f'Colony {colonyID} found in system.')
            return True
        else:
            print(f'Colony {colonyID} not found in system.')
            return False
    
    
    '''Returns the colonyStorage dictionary'''
    def getAvailability(self):
        if len(self.colonyStorage) == MAX_COLONIES:
            print("No available space in system.")
            return False
        else:
            print("Available space found in system.")
            return True
    
    '''Checks the loading zone for colonies'''
    def checkLoadingZone(self):
        paramikoSSH = self._establish_ssh_connection()
        paramikoSSH.exec_command('') # Path to executable on the Raspberry Pi
        pass


    '''Inserts a colony into the system
    colonyID: ID of the colony to be inserted
    '''
    def insertColony(self, colonyID):
        if colonyID not in self.colonyStorage:
            new_colony = Colony(colonyID=colonyID, status=True)         # Create a new colony instance
            self.colonyStorage[colonyID] = new_colony                   # Add the colony instance to the colonyStorage dictionary


    '''Removes a colony from the system
    colonyID: ID of the colony to be removed
    '''
    def extractColony(self, colonyID):
        for entry in self.colonyStorage:
            if entry['colony_instance'].id == colonyID:
                #paramikoSSH = self._establish_ssh_connection()
                #paramikoSSH.exec_command('') # Path to executable on the Raspberry Pi
           
                # If succesful, remove colonyID from colonyStorage
                self.colonyStorage.remove(entry)
                return True
            else: 
                return False
    
    '''Observes a colony
    colonyID: ID of the colony to be observed
    collects data and captures image'''
    def observeColony(self, colonyID):
        usb = self._establish_serial_connection()
        colonyInstance = self.colonyStorage.get(colonyID, None)
        print(f'Collecting data for colony {colonyID}...')
        try:
            usb.write(f'<get,{colonyID}>')
            temperature = usb.readline().decode().strip()
            colonyInstance.obsTemp = temperature
            
            '''Missing code to receive image from Pi Zero 2 w camera
            publish to topic
            receive image
            '''
        
            colonyInstance.lastObs = datetime.now().strftime("%Y-%m-%d %H:%M")  # Last observation date and time 
            print(f'Colony {colonyID} observed successfully.')
            return 1
            
        except Exception as e:
            print(f'Error: {e}')
            self.logMessage(f'Error: {e}')
            return 0

    '''Returns the observation data for a colony
    updatedColony: Colony instance with updated data
    writes data to file'''
    def getObservationData(self, updatedColony):
        try:
            colonyID = updatedColony.id
            self._updateColony(colonyID, updatedColony)
            # Retrieve the relevant data from the Colony instance
            colonyInstance = self.colonyStorage.get(colonyID, None)
            
            if colonyInstance is not None:
                # Update the data for the specific colony
                colony_data = {
                    'id': colonyInstance.id,
                    'occupied': colonyInstance.status,
                    'daytime_hours': str(colonyInstance.dayInterval),
                    'daytime_temperature': colonyInstance.dayTemp,
                    'daytime_red_light': colonyInstance.redDay,
                    'daytime_blue_light': colonyInstance.blueDay,
                    'nighttime_hours': str(colonyInstance.nightInterval),
                    'nighttime_temperature': colonyInstance.nightTemp,
                    'nighttime_red_light': colonyInstance.redNight,
                    'nighttime_blue_light': colonyInstance.blueNight,
                    'observed_temperature': colonyInstance.obsTemp,
                    'observation_interval': self.observationFrequency,
                    'experiment_start_date': str(colonyInstance.startDate),
                    'last_observation_date': str(colonyInstance.lastObsTime),
                }

                # Load existing data from the file
                with open(f'{LOCAL_PATH}filesys/colonyData.json', 'a+') as file:
                    file.seek(0)
                    try:
                        all_colonies_data = json.load(file)
                    except json.JSONDecodeError:
                        all_colonies_data = {}

                # Update the data for the specific colony in the dictionary
                all_colonies_data[f'colony{colonyID}'] = colony_data

                print("Updated data")
                print(json.dumps(all_colonies_data, indent=4))

                # Write the updated data back to the file
                with open(f'{LOCAL_PATH}filesys/colonyData.json', 'w') as file:
                    json.dump(all_colonies_data, file, indent=4)

                print(f"Data for colony {colonyID} saved successfully.")
                return 1

            else:
                print(f"Colony with ID {colonyID} not found.")
                return 0

        except Exception as e:
            print(f'Error: {e}')
            self.logMessage(f'Error: {e}')
            return 0


    '''Returns the observation footage for a colony
    colonyID: ID of the colony to be observed
    returns footage for the colony'''
    def getObservationFootage(self, colonyID):
        try:
            with open (f'{LOCAL_PATH}colony{colonyID}.txt', 'w') as file:
                # Write image data to file
                file.write(f'Colony {colonyID} image data:\n')
                for image in self.colonyStorage[colonyID]['images']:
                    file.write(f'{image}\n')
                    
            return 1
        
        except Exception as e:
            print(f'Error: {e}')
            self.logMessage(f'Error: {e}')
            return 0
        

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


    '''Sets the temperature for a colony
    colonyID: ID of the colony to be updated
    connect to arduino, set temperature and log time of change
    '''
    def setTemperature(self, colonyID):
        colonyInstance = self.colonyStorage.get(colonyID, None)
        usb = self._establish_serial_connection()
        if colonyInstance.startTime <= datetime.now().time() <= colonyInstance.dayInterval:    
            # Set day temperature
            usb.write(f'<sett,{colonyInstance.id},{colonyInstance.dayTemp}>')
            print(usb.readline().decode().strip())      # Decode and remove whitespace and print return message
            self.logMessage(f'Colony {colonyInstance.id} day temperature changed to {colonyInstance.dayTemp} at {datetime.now().time()}')    # log time of change

        else:
            # Set night temperature
            usb.write(f'sett,{colonyInstance.id},{colonyInstance.nightTemp}')
            print(usb.readline().decode().strip())     # Decode and remove whitespace and print return message
            self.logMessage(f'Colony {colonyInstance.id} night temperature changed to {colonyInstance.nightTemp} at {datetime.now().time()}')         # log time of change


    '''Sets the light for a colony
    colonyID: ID of the colony to be updated
    connect to arduino, set light and log time of change
    '''
    def setLight(self, updatedColony):
        colonyID = updatedColony.id
        self._updateColony(colonyID, updatedColony)
        colonyInstance = self.colonyStorage.get(colonyID, None)
        usb = self._establish_serial_connection()
        if colonyInstance.startTime <= datetime.now().time() <= colonyInstance.dayInterval:    
            # Set day light
            usb.write(f'<setl,{colonyInstance.id},{colonyInstance.redDay},{colonyInstance.blueDay}>')
            print(usb.readline().decode().strip())      # Decode and remove whitespace and print return message
            self.logMessage(f'Colony {colonyInstance.id} day lights changed to r:{colonyInstance.redDay} and b:{colonyInstance.blueDay} at {datetime.now().time()}')    # log time of change

        else:
            # Set night light
            usb.write(f'<setl,{colonyInstance.id},{colonyInstance.redDay},{colonyInstance.blueDay}>')
            print(usb.readline().decode().strip())      # Decode and remove whitespace and print return message
            self.logMessage(f'Colony {colonyInstance.id} day lights changed to r:{colonyInstance.redDay} and b:{colonyInstance.blueDay} at {datetime.now().time()}')    # log time of change
            
    
    '''Sets the observation interval for a colony
    colonyID: ID of the colony to be updated
    dayInterval: Day interval in hours
    nightInterval: Night interval in hours
    '''
    def setObservationInterval(self, colonyID, dayInterval, nightInterval):
        colonyInstance = self.colonyStorage.get(colonyID, None)
        colonyInstance.dayInterval = time(dayInterval, 0)
        colonyInstance.nightInterval = time(dayInterval + nightInterval, 0)
        self.logMessage(f'Colony {colonyInstance.id} day/night interval changed to {dayInterval} and {nightInterval} at {datetime.now().time()}')    # log time of change
        

    '''Sets the observation interval for all colonies	
    observationFrequency: Observation interval in hours
    '''
    def setObservationFrequency(self, observationFrequency):
        self.observationFrequency = observationFrequency
        self.logMessage(f'Observation interval for all colonies changed to {observationFrequency} at {datetime.now().time()}')    # log time of change
        

    def pauseObservation(colonyID):
        # Call a method from Pi to pause observation
        pass
    

    '''Logs a message to the logfile
    msg: Message to be logged
    '''
    def logMessage(msg, *args):
        # log messages in logfile
        with open(f'{LOCAL_PATH}filesys/logfile.txt', 'a') as file:
            file.write(f'{datetime.now().time()}: {msg}\n')
    

    """Display the storage of the colony.
    Prints the string representation of each colony instance in the colony storage.
    """
    def displayColonyStorage(self, colonyID=None):
        if colonyID is not None:
            colony_instance = self.colonyStorage.get(colonyID)
            if colony_instance is not None:
                print(colony_instance)
            else:
                self.logMessage(f"Colony with ID {colonyID} not found in storage.")
                print(f"Colony {colonyID} - status: Not Occupied")
        else:
            for colony_instance in self.colonyStorage.items():
                print(colony_instance)


    """Update an existing colony instance in the colonyStorage.
    colonyID: ID of the colony to be updated
    updatedColony: Colony instance with updated data
    file: If True, update colony from file
    """
    def _updateColony(self, colonyID, updatedColony, file=False):
        # Update an existing colony instance in the colonyStorage
        if colonyID in self.colonyStorage and file is False:
            existing_colony_instance = self.colonyStorage[colonyID]
            existing_colony_instance.updateAttributes(updatedColony)
            print(f"Colony {colonyID} updated successfully.")
        elif colonyID in self.colonyStorage and file is True:
            existing_colony_instance = self.colonyStorage[colonyID]
            existing_colony_instance.updateAttributesFromFile(file)
            print(f"Colony {colonyID} updated successfully.")
        else:
            print(f"Colony with ID {colonyID} not found.")
            

master = Master(1)
colony = Colony(1)
print(f'Before inserting colony: {master.colonyStorage}')
master.displayColonyStorage(colony.id)
master.insertColony(colonyID=colony.id)
print(f'After inserting colony: {master.colonyStorage}')
master.displayColonyStorage(colonyID = colony.id)
master.getObservationData(colony)
colony.redDay = 10
colony.blueDay = 15
colony.redNight = 20
colony.blueNight = 25
master.setLight(colony)