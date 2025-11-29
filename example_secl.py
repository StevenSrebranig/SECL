"""
example_secl.py

Demonstration of the SECLController regulating a noisy metric.
Run with:  python example_secl.py
"""

import random
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

    for t in range(1, 1001):
        # Simulate a noisy measurement (e.g., power) with slow drift.
        true_level += random.uniform(-0.001, 0.001)  # slow wander
        noise = random.gauss(0.0, 0.1)
        measurement = gain * true_level + noise

        # Let SECL adapt the gain based on the measurement.
        gain = ctrl.update(measurement)

        if t % 100 == 0:
            print(f"t={t:4d}, measurement={measurement: .3f}, gain={gain: .3f}")

if __name__ == "__main__":
    simulate()
