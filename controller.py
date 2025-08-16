# PID controller class
# Takes error and outputs motor commands or force/torque

import numpy as np


class PIDController:
    def __init__(self, Kp=1.0, Ki=0.0, Kd=0.0, target_altitude=10.0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.integral = 0.0
        self.prev_error = 0.0
        self.target_altitude = target_altitude

    def reset(self):
        self.integral = 0.0
        self.prev_error = 0.0

    def update(self, state, dt):
        """PID control for altitude only"""
        current_altitude = state["position"][2]
        error = self.target_altitude - current_altitude

        # Integral & Derivative
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0.0
        self.prev_error = error

        # PID output (thrust)
        thrust = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

        # control vector = [roll, pitch, thrust, yaw]
        return np.array([0.0, 0.0, thrust, 0.0])
