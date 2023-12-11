from datetime import datetime

class Colony:
    def __init__(self, colonyID, redDay=0, blueDay=0,
                 redNight=0, blueNight=0, dayTemp=15,
                 nightTemp=15, dayInterval="01:00:00", nightInterval="01:00:00"):

        self.id = colonyID      # Colony ID
        # Colony settings
        self.dayTemp = dayTemp
        self.nightTemp = nightTemp
        self.obsTemp = 0
        self.redDay = redDay
        self.redNight = redNight
        self.blueDay = blueDay
        self.blueNight = blueNight

        # Time stuff
        self.startTime = datetime.strptime("00:00:00", "%H:%M:%S").time()                 # Day starts at 00:00
        self.startDate = datetime.now().date()      # Current date
        self.lastObsTime = datetime.now().strftime("%Y-%m-%d %H:%M")  # Last observation date and time
        self.dayInterval = datetime.strptime(dayInterval, "%H:%M:%S").time()     # Day interval
        self.nightInterval = datetime.strptime(nightInterval, "%H:%M:%S").time() # Night interval

    def __str__(self):
        # return colony attribute values
        return f"Colony {self.id}:\n" \
               f"Day temp: {self.dayTemp}\n" \
               f"Night temp: {self.nightTemp}\n" \
                   f"Obs temp: {self.obsTemp}\n" \
               f"Last observation: {self.lastObsTime}\n" \
               f"Day interval: {self.dayInterval}\n" \
               f"Night interval: {self.nightInterval}\n" \
               f"Red day: {self.redDay}\n" \
               f"Red night: {self.redNight}\n" \
               f"Blue day: {self.blueDay}\n" \
               f"Blue night: {self.blueNight}\n"