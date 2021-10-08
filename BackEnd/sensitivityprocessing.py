"""

@author:    Philipp
            philipp.matten@meduniwien.ac.at

@copyright: Medical University of Vienna,
            Center for Medical Physics and Biomedical Engineering

"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt

from octdatafilemanager import OctDataFileManager as OctImport


def load_detector_signals(path: str) -> np.ndarray :
    """ Load all *.bin-files from path """
    IM = OctImport()
    files = glob.glob(os.path.join(IM._tk_folder_selection() + "/*.bin"))
    scans = []
    for file in files :
        scans.append(np.fromfile(file, dtype='>u2'))
    return np.asarray(np.stack(scans, axis=0))

def reconstruct_aScans(data_in: np.ndarray) -> np.ndarray:
    """ Performs SS-OCT reconstruction on array """
    # average stack
    stack = np.mean(data_in, axis=1)
    aLen = stack.shape[0]
    # windowing
    stack = np.multiply( stack, np.hanning(aLen) )
    # abs of iFFT of padded array
    stack = np.abs( np.fft.ifft( np.pad( stack, pad_with=(aLen, 0), mode='constant', constant_values=0 ) ) )
    # scale of first half of complex conjugate F^-1(signal) to 8Bit 
    stack = 20 * np.log10( np.abs(stack[:aLen]) )
    # return a-Scan scaled within dynamic range 
    return np.asarray( 255 * ( (stack - 77) / 63.75 ) )

def plot_aScan():
    """TBD"""
    pass

def plot_aScans():
    """TBD"""
    pass


def run():
    res = load_detector_signals(r"C:\Users\PhilippsLabLaptop\Documents\Data\TestFolderAtsDetectorSignals")
    print(res)
    recon_aScan = reconstruct_aScans(res)

if __name__ == '__main__':
    run()