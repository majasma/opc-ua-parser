import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":

    # Generate 1000 evenly spaced values between 0 and 300
    x = np.linspace(0, 300, 100)

    # Generate a sine wave with frequency of 2 and amplitude of 5
    y = 5 * np.sin(1 * np.pi * 2 * x / 300)

    # Scale the y-axis values to range between 0 and 10
    y = (y + 5) * 10 / 10

    print(y)