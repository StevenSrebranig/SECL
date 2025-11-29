"""
Statistical-Envelope Control Loop (SECL)

Minimal reference implementation of the SECL pattern:

- Maintain a rolling window of a noisy metric (e.g., output power, SNR, error).
- Estimate a statistical envelope (lower / upper quantiles) from that window.
- Adjust a control gain so the metric stays inside the envelope rather than
  converging to a fixed setpoint.

This is a didactic implementation to illustrate the pattern, not a drop-in
replacement for any specific hardware AGC design.
"""

from collections import deque
from typing import Deque, List


def _quantile(xs: List[float], q: float) -> float:
    """
    Simple quantile helper (q in [0, 1]) without external libraries.
    Uses sorted list and linear interpolation between neighbors.
    """
    if not xs:
        raise ValueError("Cannot compute quantile of empty list.")
    xs_sorted = sorted(xs)
    n = len(xs_sorted)
    if n == 1:
        return xs_sorted[0]

    # position in [0, n-1]
    pos = q * (n - 1)
    i = int(pos)
    frac = pos - i

    if i >= n - 1:
        return xs_sorted[-1]
    return xs_sorted[i] * (1.0 - frac) + xs_sorted[i + 1] * frac


class SECLController:
    """
    Statistical-Envelope Control Loop controller.

    Each call to update(measurement) returns the current control gain.
    The controller adapts gain to keep the metric inside a rolling
    statistical envelope defined by lower/upper quantiles.
    """

    def __init__(
        self,
        window_size: int = 200,
        lower_q: float = 0.25,
        upper_q: float = 0.75,
        step_fraction: float = 0.05,
        initial_gain: float = 1.0,
        min_gain: float = 0.1,
        max_gain: float = 10.0,
        warmup_samples: int = 20,
    ) -> None:
        """
        Args:
            window_size: number of recent samples used to estimate envelope.
            lower_q: lower quantile for envelope (e.g., 0.25).
            upper_q: upper quantile for envelope (e.g., 0.75).
            step_fraction: fractional change applied to gain when correcting.
            initial_gain: starting gain value.
            min_gain: minimum allowed gain.
            max_gain: maximum allowed gain.
            warmup_samples: number of samples to collect before adapting.
        """
        if not (0.0 < lower_q < upper_q < 1.0):
            raise ValueError("Require 0 < lower_q < upper_q < 1.")

        self.window_size = int(window_size)
        self.lower_q = float(lower_q)
        self.upper_q = float(upper_q)
        self.step_fraction = float(step_fraction)
        self.gain = float(initial_gain)
        self.min_gain = float(min_gain)
        self.max_gain = float(max_gain)
        self.warmup_samples = int(warmup_samples)

        self._history: Deque[float] = deque(maxlen=self.window_size)

    def update(self, measurement: float) -> float:
        """
        Update the controller with a new metric sample.

        Args:
            measurement: observed metric value (e.g., power, error).

        Returns:
            Current control gain after any adaptation.
        """
        self._history.append(float(measurement))

        # Not enough data yet to estimate envelope: hold gain.
        if len(self._history) < self.warmup_samples:
            return self.gain

        xs = list(self._history)
        low = _quantile(xs, self.lower_q)
        high = _quantile(xs, self.upper_q)

        # If metric is too high, reduce gain.
        if measurement > high:
            self.gain *= (1.0 - self.step_fraction)
        # If metric is too low, increase gain.
        elif measurement < low:
            self.gain *= (1.0 + self.step_fraction)
        # If inside envelope, leave gain unchanged.

        # Clamp gain to safe range.
        if self.gain < self.min_gain:
            self.gain = self.min_gain
        elif self.gain > self.max_gain:
            self.gain = self.max_gain

        return self.gain
