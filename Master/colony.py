from datetime import datetime, time
import json

class Colony:
    def __init__(self, colonyID, status=False, redDay=0, blueDay=0, 
                 redNight=0, blueNight=0, dayTemp=0, 
                 nightTemp=0, dayInterval=0, nightInterval=0):
        
        self.id = colonyID      # Colony ID
        self.status = status    # Set to True if occupied

        # Colony settings
        self.dayTemp = dayTemp
        self.nightTemp = nightTemp
        self.obsTemp = 0 
        self.redDay = redDay
        self.redNight = redNight
        self.blueDay = blueDay
        self.blueNight = blueNight
        
        # Time stuff
        self.startTime = time(0, 0)                 # Day starts at 00:00
        self.startDate = datetime.now().date()      # Current date
        self.lastObsTime = datetime.now().strftime("%Y-%m-%d %H:%M")  # Last observation date and time        
        self.dayInterval = time(dayInterval, 0)     # Day interval
        self.nightInterval = time(nightInterval, 0) # Night interval
    
    def __str__(self):
        return f"Colony {self.id} - Status: {'Occupied' if self.status else 'Not Occupied'}"


    def updateAttributes(self, updatedColony):
        self.status = updatedColony.status
        self.dayTemp = updatedColony.dayTemp
        self.nightTemp = updatedColony.nightTemp
        self.redDay = updatedColony.redDay
        self.redNight = updatedColony.redNight
        self.blueDay = updatedColony.blueDay
        self.blueNight = updatedColony.blueNight
        self.dayInterval = updatedColony.dayInterval
        self.nightInterval = updatedColony.nightInterval


    def updateAttributesFromFile(self, file_path='settings.json'):
        # Read settings from the specified JSON file and load them into the colony object
        with open(file_path, 'r') as f:
            settings = json.load(f)

            # Update attributes based on the settings
            settings = settings.get(f'colony{self.id}', {})
            if settings is not None:
                self.status = settings.get('occupied', self.status)
                self.dayTemp = settings.get('daytime_temperature', self.dayTemp)
                self.nightTemp = settings.get('nighttime_temperature', self.nightTemp)
                self.redDay = settings.get('daytime_red_light', self.redDay)
                self.redNight = settings.get('nighttime_red_light', self.redNight)
                self.blueDay = settings.get('daytime_blue_light', self.blueDay)
                self.blueNight = settings.get('nighttime_blue_light', self.blueNight)
                self.dayInterval = time(settings.get('daytime_hours', self.dayInterval.hour), 0)
                self.nightInterval = time(settings.get('nighttime_hours', self.nightInterval.hour), 0)
            else:
                print(f'No settings found for colony {self.id}')            

    def _updateInstanceVariables(self, settings=None):

            # Update attributes from instance variables
            self.status = self.status
            self.dayTemp = self.dayTemp
            self.nightTemp = self.nightTemp
            self.redDay = self.redDay
            self.redNight = self.redNight
            self.blueDay = self.blueDay
            self.blueNight = self.blueNight
            self.dayInterval = self.dayInterval
            self.nightInterval = self.nightInterval
