# Importing libraries
import matplotlib.pyplot as plt
import numpy as np

# Define function to plot normal
def plotCurrents(currents, title):
    coefficients = np.polyfit(duty_cycles, currents_red, 1)
    line_of_best_fit = np.polyval(coefficients, duty_cycles)

    plt.plot(duty_cycles, currents, marker='o', linestyle='-', color='b', label='Data')
    plt.plot(duty_cycles, line_of_best_fit, linestyle='--', color='r', label=f'Linear Regression: {coefficients[0]:.4f}x + {coefficients[1]:.4f}')
    plt.xlabel('Duty Cycle (%)')
    plt.ylabel('Current (mA)')
    plt.ylim(-2, 260)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

# Define function to plot linear region
def plotCurrentsLinear(currents, title):
    coefficients = np.polyfit(duty_cycles[10:28], currents_red[10:28], 1)
    line_of_best_fit = np.polyval(coefficients, duty_cycles)
    plt.plot(duty_cycles[10:28], currents[10:28], marker='o', linestyle='-', color='b', label='Data')
    plt.plot(duty_cycles, line_of_best_fit, linestyle='--', color='r', label=f'Linear Regression: {coefficients[0]:.4f}x + {coefficients[1]:.4f}')
    plt.xlabel('Duty Cycle (%)')
    plt.ylabel('Current (mA)')
    plt.title(title)
    plt.xlim(48, 86)
    plt.ylim(0, 200)
    plt.legend()
    plt.grid(True)
    plt.show()

# Define function to plot relative flux
def plotRelativeFlux(relative_flux, title):
    duty_cycles_relative = np.linspace(duty_cycles[10], duty_cycles[28], len(relative_flux))
    coefficients = np.polyfit(duty_cycles_relative, relative_flux, 1)
    line_of_best_fit = np.polyval(coefficients, duty_cycles_relative)

    plt.plot(duty_cycles_relative, relative_flux, marker='o', linestyle='-', color='g', label=f'Relative Flux')
    plt.plot(duty_cycles_relative, line_of_best_fit, linestyle='--', color='r', label=f'Linear Regression: {coefficients[0]:.4f}x + {coefficients[1]:.4f}')
    plt.xlabel('Duty Cycle (%)')
    plt.ylabel('Relative Flux (%)')
    plt.title(title)
    plt.ylim(0, 100)
    plt.legend()
    plt.grid(True)
    plt.show()

# Dataset for duty cycles
duty_cycles = [30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100]

# Defined relative flux
relative_flux = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# Dataset for currents
currents_red = []
with open('red_led_current.txt', 'r') as f:
    currents_red = [float(line.strip()) for line in f]

currents_blue = []
with open('blue_led_current.txt', 'r') as f:
    currents_blue = [float(line.strip()) for line in f]

currents_temp = []
with open('temp_current.txt', 'r') as f:
    currents_temp = [float(line.strip()) for line in f]


# Plotting 
#plotCurrents(currents_red, 'Red-Led: Duty Cycle (%) vs Current')

# Use function to plot linear region
#plotCurrentsLinear(currents_red, 'Red-Led: Linear Region, Duty Cycle vs Current')

# Plotting relative flux
#plotRelativeFlux(relative_flux, 'Red-Led: Duty Cycle vs Relative Flux')

# Blue led
#plotCurrents(currents_blue, 'Blue-Led: Duty Cycle (%) vs Current')

# Use function to plot linear region
#plotCurrentsLinear(currents_blue, 'Blue-Led: Linear Region, Duty Cycle vs Current')

# Plotting relative flux
#plotRelativeFlux(relative_flux, 'Blue-Led: Duty Cycle vs Relative Flux')

# Heating element
plotCurrents(currents_temp, 'Heating-Element: Duty Cycle (%) vs Current')

# Use function to plot linear region
plotCurrentsLinear(currents_temp, 'Heating-Element: Linear Region, Duty Cycle vs Current')
