# Real-time plots of position, attitude, etc.
# Visualizes state history (live or after sim)

import matplotlib.pyplot as plt


def altitude_plot(times, quad_positions_z):

    plt.plot(times, quad_positions_z)
    plt.xlabel("Time(s)")
    plt.ylabel("Altitude(m)")
    plt.title("Quadrotor Altitude Response")
    plt.grid()
    plt.show()
