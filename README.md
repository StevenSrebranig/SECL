# Statistical-Envelope Control Loop (SECL)

A distribution-bound control pattern that regulates a noisy metric using a
rolling statistical envelope rather than a fixed setpoint.

- **No explicit setpoint**
- **No plant model**
- **Drift-stable by design**
- **Constant-time updates per sample**
- **Works with noisy, nonstationary signals**

The core idea:

> Maintain a rolling window of recent metric values, estimate a statistical
> envelope (e.g., 25th–75th percentiles), and adapt a control gain so the
> metric stays inside that envelope.

## Files

- `secl.py` – minimal reference implementation of a SECL controller.
- `example_secl.py` – small demo script showing SECL regulating a noisy metric.

## Reference

Whitepaper (Zenodo DOI):

- https://doi.org/10.5281/zenodo.17715671

## License

MIT License – free for commercial and noncommercial use, with attribution.
