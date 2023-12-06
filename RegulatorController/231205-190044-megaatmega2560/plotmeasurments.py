#import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

# plot the following data:
duty = [0, 10, 20, 30, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
current = [2, 2.0, 2.0, 2.0, 4.0, 10.5, 24, 35, 51.0, 72, 100, 134, 157, 182.7, 260, 260, 260] 

# Plot the data
plt.plot(duty, current, 'ro')
plt.axis([0, 100, 0, 300])
plt.xlabel('Duty Cycle (%)')
plt.ylabel('Current (mA)')
plt.title('Current vs Duty Cycle')
plt.show()
