"""Analytic SCI and CSM reference curves for pion and kaon distributions."""
from __future__ import annotations
import numpy as np

# (normalization, x exponent, (1-x) exponent, polynomial coefficients in exp)
PARAMETERS = {
    ('pion', 'valence'): ((1.05768962, .58802146, 1.35849983, ()),
                          (2.59379870, .89962791, 2.31693918, ())),
    ('pion', 'glue'): ((19.03952954, 1.19326122, 2.62967187, ()),
                       (27.92448986, 1.32185105, 3.56511509, ())),
    ('kaon', 'valence'): ((np.exp(.34178409), .65570682, 2.06317399,
                          (-.31769991, 2.52734638, -4.57612513, 3.68841809)),
                         (np.exp(1.00371903), .87228618, 5.32960474,
                          (2.19958339, 4.54166333, -6.53284156, 7.48602113))),
    ('kaon', 'glue'): ((np.exp(1.34369499), .71136305, 2.28073064,
                       (5.47288434, -12.33487604, 13.41377199, -6.34889462)),
                      (np.exp(2.90666107), 1.28147620, -.74394435,
                       (-.52070446, -18.69048583, 30.88826911, -24.79239594))),
}


def evaluate(channel, component, x):
    """Evaluate SCI, CSM and their midpoint; return three arrays at input x.

    Args:
        channel, component, x: Inputs and configuration for this operation.
    Returns:
        Computed data or saved file paths, as described above.
    """
    x = np.asarray(x, dtype=float)
    output = []
    for amplitude, power_x, power_one_minus_x, terms in PARAMETERS[channel, component]:
        polynomial = sum(value * x ** (degree + 1) for degree, value in enumerate(terms))
        output.append(amplitude * x ** power_x * (1 - x) ** power_one_minus_x * np.exp(polynomial))
    return output[0], output[1], (output[0] + output[1]) / 2
