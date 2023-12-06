import matplotlib.pyplot as plt
import numpy as np

# Dataset
duty_cycles = [30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100]
# open and assign from file
currents = []
with open('red_led_current.txt', 'r') as f:
    currents = [float(line.strip()) for line in f]



# Perform linear regression
coefficients = np.polyfit(duty_cycles, currents, 1)
line_of_best_fit = np.polyval(coefficients, duty_cycles)

# Plotting
plt.plot(duty_cycles, currents, marker='o', linestyle='-', color='b', label='Data')
plt.plot(duty_cycles, line_of_best_fit, linestyle='--', color='r', label=f'Linear Regression: {coefficients[0]:.4f}x + {coefficients[1]:.4f}')
plt.xlabel('Duty Cycle')
plt.ylabel('Current (mA)')
plt.title('Red-Led: Duty Cycle vs Current with Linear Regression')
plt.legend()
plt.grid(True)
plt.show()