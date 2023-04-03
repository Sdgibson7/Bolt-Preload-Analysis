"""__thor_model__.py: Stores the thor model and coefficients."""

__author__      = "Samuel Gibson"

import numpy as np
from multipledispatch import dispatch

# Use placeholder MATLAB model for now...
__coefficients = {
    "a": float(9.802),
    "b": float(-0.099),
    "c": float(96.78),
    "d": float(-0.000446),
}

_SEALANT = "sealant"
_PLATE_MATERIAL = "plate material"
_PARAMETER3 = "parameter3"
_PARAMETER4 = "parameter4"

__values = {
    _SEALANT: {
        "v1": float(2.0),
        "v2": float(3.0),
        "v3": float(5.0)
    },
    _PLATE_MATERIAL: {
        "aluminum": float(5.0),
        "carbon fiber": float(6.2),
        "v3": float(10.0)
    },
    _PARAMETER3: {
        "v1": float(1.1),
        "v2": float(1.2),
        "v3": float(1.3)
    },
    _PARAMETER4: {
        "v1": float(1.0),
        "v2": float(2.0),
        "v3": float(3.0)
    }
}

'''Returns a list of values for the given parameter'''
def get_values(name):
    return list(__values[name].keys())

'''Takes an ndarray of x values and calculates the corresponding y values, using our model. Returns an ndarray.'''
@dispatch(np.ndarray)
def exp_model(plot_x):
    return (__coefficients["a"]*np.exp(__coefficients["b"] * plot_x)) + (__coefficients["c"]*np.exp(__coefficients["d"] * plot_x))

'''Takes an ndarray of x values and calculates the corresponding y values, using our model. Applies a modifier to each coefficient of the model for a,b,c,d. Returns an ndarray.'''
@dispatch(np.ndarray, str, str, str, str)
def exp_model(plot_x, a, b, c, d):
    a_new = __coefficients["a"] * __values[_SEALANT][a]
    b_new = __coefficients["b"] * __values[_PLATE_MATERIAL][b]
    c_new = __coefficients["c"] * __values[_PARAMETER3][c]
    d_new = __coefficients["d"] * __values[_PARAMETER4][d]
    
    return (a_new*np.exp(b_new * plot_x)) + ((c_new)*np.exp(d_new * plot_x))