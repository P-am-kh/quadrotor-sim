# Entry point: runs the simulation
# Initializes objects and runs the time loop

from quadrotor import Quadrotor
from controller import PIDController
from plotter import altitude_plot


def main():

    mass, dt = inputs_from_user()

    quad = Quadrotor(mass)
    controller = PIDController(Kp=2.0, Ki=0.1, Kd=0.5, target_altitude=10.0)

    simulation_time = 20.0
    steps = int(simulation_time / dt)
    times = []
    quad_positions_z = []

    for step in range(steps):
        control_input = controller.update(quad.state, dt)
        state = quad.update(control_input, dt)

        print(
            f"Time: {step*dt:.2f}s, Position: {state['position']}, Orientation (z): {state['orientation'][2]}"
        )

        times.append(dt * step)
        quad_positions_z.append(state["position"][2])

    altitude_plot(times, quad_positions_z)


def inputs_from_user():

    while True:
        dt_input = input("please enter time step(s):  ")
        mass_input = input("please enter the mass(kg):  ")

        try:
            dt = float(dt_input)
            mass = float(mass_input)

            if dt > 0 and mass > 0:
                break
            else:
                print("time step and mass must be more than 0")

        except ValueError:
            print("Invalid input. Using default time step = 0.01 s and mass = 1.0 kg")
            dt = 0.01
            mass = 1
            break

    return mass, dt


if __name__ == "__main__":
    main()
