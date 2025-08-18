import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
)
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from quadrotor import Quadrotor
from PyQt6.QtCore import QTimer


class GLWidget(QOpenGLWidget):
    def initializeGL(self):
        pass

    def paintGL(self):
        pass

    def resizeGL(self, w, h):
        pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quadrotor Simulator")
        self.setGeometry(100, 100, 800, 600)

        # central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # --- input fields ---
        self.dt_input = QLineEdit()
        self.dt_input.setPlaceholderText("Enter time step (dt)")
        layout.addWidget(QLabel("Time step (dt):"))
        layout.addWidget(self.dt_input)

        self.mass_input = QLineEdit()
        self.mass_input.setPlaceholderText("Enter mass (kg)")
        layout.addWidget(QLabel("Mass (kg):"))
        layout.addWidget(self.mass_input)

        self.ok_button = QPushButton("OK")
        layout.addWidget(self.ok_button)
        self.ok_button.clicked.connect(self.save_inputs)

        self.start_button = QPushButton("Start Simulation")
        layout.addWidget(self.start_button)
        self.start_button.clicked.connect(self.start_simulation)

        self.stop_button = QPushButton("Stop Simulation")
        layout.addWidget(self.stop_button)
        self.stop_button.clicked.connect(self.stop_simulation)

        self.timer = QTimer()
        self.timer.timeout.connect(self.simulation_step)

        # OpenGL widget
        self.gl_widget = GLWidget()
        layout.addWidget(self.gl_widget)

        # Buttons
        self.btn_takeoff = QPushButton("Take Off")
        layout.addWidget(self.btn_takeoff)
        self.btn_takeoff.clicked.connect(self.takeoff)

        # default values
        self.dt = 0.01
        self.mass = 1.0
        self.quad = None

    def save_inputs(self):
        try:
            dt = float(self.dt_input.text())
            mass = float(self.mass_input.text())
            if dt <= 0 or mass <= 0:
                raise ValueError
            self.dt = dt
            self.mass = mass
            self.quad = Quadrotor(mass)
            QMessageBox.information(self, "Inputs Saved", f"dt={dt}, mass={mass}")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter positive numbers.")

    def takeoff(self):
        if not self.quad:
            QMessageBox.warning(self, "Error", "Please enter dt and mass first.")
            return
        control_input = np.array([0.0, 0.0, 15.0, 0.0])
        new_state = self.quad.update(control_input, self.dt)
        print("State after takeoff:", new_state["position"])

    def start_simulation(self):
        if not self.quad:
            QMessageBox.warning(self, "Error", "Please enter dt and mass first.")
            return
        self.timer.start(int(self.dt * 1000))  # تبدیل dt به میلی‌ثانیه

    def stop_simulation(self):
        self.timer.stop()

    def simulation_step(self):
        control_input = np.array([0.0, 0.0, 15.0, 0.0])
        new_state = self.quad.update(control_input, self.dt)
        print("State:", new_state["position"])


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
