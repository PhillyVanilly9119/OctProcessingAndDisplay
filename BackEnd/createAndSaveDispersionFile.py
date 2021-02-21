# TODO: import backend functions from OCT processing scripts to keep consistency throughout the code
# -> Open question: How to import the functions from the files from different repos

# Proprietary imports
import os
import numpy as np

# Custom imports
# ...

def create_dispersion_vector(a_len, coeffs) :
    """
    Creates a complex valued polynominal vector
    """
    return np.asarray(np.polyval(coeffs, np.linspace(-0.5, 0.5, a_len)))

def create_complex_dispersion_vector(vector, key='hann') :
    a_len = np.shape(vector)[0]
    if key == 'hann' :
        window = np.hanning(a_len)
    else :
        print(f"key {key} is not yet implemented")
    x = np.multiply(window, np.cos(vector))
    y = np.multiply(window, np.sin(vector))
    output = np.zeros(2 * a_len, dtype=np.float32)
    for i in range(a_len) :
        output[2 * i - 1] = x[i]
        output[2 * i] = y[i]
    # Write to file
    # Check if saving was successful

def save_dispersion_vector_to_file(vector, path, use_fixed_path=True) :
    """
    Saves complex-valued dispersion vector 
    """
    pass
