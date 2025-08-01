# PID controller class
# Takes error and outputs motor commands or force/torque

import numpy as np


class PIDController:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = np.array(Kp)
        self.Ki = np.array(Ki)
        self.Kd = np.array(Kd)
        self.integral = np.zeros(3)
        self.prev_error = np.zeros(3)

    def reset(self):
        self.integral[:] = 0
        self.prev_error[:] = 0

    def compute(self, target, current, dt):
        """
        Compute PID output to reduce error between target and current value.
        Inputs:
            - target: desired value (3D)
            - current: current value (3D)
            - dt: time step
        Output: control output (3D)
        """

        error = target - current
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        self.prev_error = error

        output = self.Kp * error + self.Kd * derivative + self.Ki * self.integral

        return output
