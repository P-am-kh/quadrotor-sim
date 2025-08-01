# Class for dynamics and state updates

"""
Holds the physical model (mass, inertia, etc.)

Computes the 6-DOF dynamics

Updates position, velocity, orientation

"""

import numpy as np


class Quadrotor:
    def __init__(self, mass=1.0, inertia=None):

        self.mass = mass
        self.inertia = inertia if inertia is not None else np.diag([0.01, 0.01, 0.02])

        self.position = np.zeros(3)  # [x, y, z] in world frame
        self.velocity = np.zeros(3)  # [vx, vy, vz] in world frame
        self.orientation = np.eye(3)  # Rotation matrix (body to world)
        self.omega = np.zeros(3)  # Angular velocity in body frame

    def reset(self):
        self.position[:] = 0
        self.velocity[:] = 0
        self.orientation = np.eye(3)
        self.omega[:] = 0

    def step(self, thrust_body, torque_body, dt):
        """
        Update the state of the quadrotor using the applied thrust and torque.
        thrust_body: np.array([Fx, Fy, Fz]) in body frame
        torque_body: np.array([τx, τy, τz]) in body frame
        dt: timestep (s)
        """

        g = np.array([0, 0, -9.81])  # gravity in world frame

        # Convert thrust from body frame to world frame
        thrust_world = self.orientation @ thrust_body

        # Acceleration = (thrust + gravity) / mass
        accel = thrust_world / self.mass + g

        # Update velocity and position (Euler integration)
        self.velocity += accel * dt
        self.position += self.velocity * dt
        pass
