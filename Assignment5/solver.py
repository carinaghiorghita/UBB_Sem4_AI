# -*- coding: utf-8 -*-
from constants import *
"""
In this file your task is to write the solver function!

"""

def fuzzify(x, start, peak, end):
    if start is not None and start <= x < peak:
        return (x - start) / (peak - start)
    elif end is not None and peak <= x < end:
        return (end - x) / (end - peak)
    elif start is None and x <= peak:
        return 1
    elif end is None and x >= peak:
        return 1
    else:
        return 0

def getValues(val, valrange):
    values = dict()
    for key in valrange:
        values[key] = fuzzify(val, *valrange[key])
    return values

def solver(t,w):
    """
    Parameters
    ----------
    t : TYPE: float
        DESCRIPTION: the angle theta
    w : TYPE: float
        DESCRIPTION: the angular speed omega

    Returns
    -------
    F : TYPE: float
        DESCRIPTION: the force that must be applied to the cart
    or

    None :if we have a division by zero

    """
    peakval = {key: value[1] for key, value in F_RANGE.items()}

    theta = getValues(t, THETA_RANGE)
    omega = getValues(w, OMEGA_RANGE)

    fValues = dict()
    for thetaKey in FUZZY_TABLE:
        for omegaKey, f in FUZZY_TABLE[thetaKey].items():
            val = min(theta[thetaKey],omega[omegaKey])
            if f not in fValues:
                fValues[f] = val
            else:
                fValues[f] = max(val,fValues[f])
    s = sum(fValues.values())
    if s == 0:
        return None
    return sum(fValues[fSet] * peakval[fSet] for fSet in fValues.keys()) / s
