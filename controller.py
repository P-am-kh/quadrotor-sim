from Quadrotor_Simulation import QuadrotorSimulator
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class QuadrotorApp:
    def __init__(self, root):
        # ... (previous initialization code)

        # Setup plot
        self.setup_plot()

    def setup_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.ax.set_title("Quadrotor Position")
        self.ax.set_xlabel("X Position (m)")
        self.ax.set_ylabel("Z Position (m)")
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(0, 10)
        self.ax.grid(True)

        # Initial point
        (self.plot_point,) = self.ax.plot(0, 0, "ro", markersize=10)

        # Embed plot in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=10)

    def update_plot(self):
        x, _, z = self.simulator.position
        self.plot_point.set_data(x, z)
        self.canvas.draw()

    def move(self, direction):
        pos = self.simulator.update_position(direction)
        self.status_label.config(text=f"Moving {direction}")
        self.position_label.config(text=self.get_position_text())
        self.update_plot()

    def takeoff(self):
        pos = self.simulator.takeoff()
        self.status_label.config(text="Taking off...")
        self.position_label.config(text=self.get_position_text())
        self.update_plot()

    def land(self):
        pos = self.simulator.land()
        self.status_label.config(text="Landing...")
        self.position_label.config(text=self.get_position_text())
        self.update_plot()
