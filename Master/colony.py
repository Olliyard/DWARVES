from datetime import datetime, time
import json

class Colony:
    def __init__(self, colonyID, status=False, redDay=0, blueDay=0, 
                 redNight=0, blueNight=0, dayTemp=15, 
                 nightTemp=15, dayInterval=1, nightInterval=1):
        
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

    def __setitem__(self, key, value):
        # Assuming settings are stored as attributes in the Colony instance
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Invalid key: {key}")

    def update(self, attributes):
        for key, value in attributes.items():
            setattr(self, key, value)

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
                self.dayInterval = datetime.strptime(settings.get('daytime_hours', f"{self.dayInterval.hour}:00:00"), "%H:%M:%S").time()
                self.nightInterval = datetime.strptime(settings.get('nighttime_hours', f"{self.nightInterval.hour}:00:00"), "%H:%M:%S").time()
            else:
                print(f'No settings found for colony {self.id}')
