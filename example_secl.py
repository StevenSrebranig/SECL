"""
example_secl.py

Demonstration of the SECLController regulating a drifting, noisy metric.
Run with:  python example_secl.py

This example visualizes:
- true underlying level (slow random drift)
- observed measurements (noisy output)
- adaptive gain applied by SECL
"""

import random
import matplotlib.pyplot as plt
from secl import SECLController

def simulate():
    # "True" underlying level we are trying to keep in a reasonable range.
    true_level = 1.0

    # Create SECL controller.
    ctrl = SECLController(
        window_size=200,
        lower_q=0.25,
        upper_q=0.75,
        step_fraction=0.05,
        initial_gain=1.0,
    )

    gain = 1.0

    # For plotting
    true_levels = []
    measurements = []
    gains = []

    for t in range(1, 1001):
        # Simulate a noisy measurement (e.g., power) with slow drift.
        true_level += random.uniform(-0.001, 0.001)  # slow wander
        noise = random.gauss(0.0, 0.1)
        measurement = gain * true_level + noise

        # Let SECL adapt the gain based on the measurement.
        gain = ctrl.update(measurement)

        # Save history
        true_levels.append(true_level)
        measurements.append(measurement)
        gains.append(gain)

        # Periodic text output
        if t % 100 == 0:
            print(f"t={t:4d}, measurement={measurement: .3f}, gain={gain: .3f}")

    # ---- Plot results ----
    plt.figure(figsize=(10, 6))
    plt.plot(true_levels, label="True underlying level (drifting)", alpha=0.6)
    plt.plot(measurements, label="Observed measurement (SECL-stabilized)", linewidth=2)
    plt.plot(gains, label="Adaptive gain", linestyle="--")
    plt.legend()
    plt.title("SECL in Action: Stabilizing a Drifting Noisy Metric")
    plt.xlabel("Time step")
    plt.ylabel("Value")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    simulate()
