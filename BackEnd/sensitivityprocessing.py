"""

@author:    Philipp
            philipp.matten@meduniwien.ac.at

@copyright: Medical University of Vienna,
            Center for Medical Physics and Biomedical Engineering

"""

import os
import glob
from turtle import back
import numpy as np
from numba import njit
import matplotlib.pyplot as plt

from octdatafilemanager import OctDataFileManager as OctImport
from octreconstructionmanager import OctReconstructionManager


def load_detector_signals(path: str) -> np.ndarray:
    """ Load all *.bin-files from path """
    files = glob.glob(os.path.join(path + "/*.bin"))
    scans = []
    for file in files:
        scans.append(np.fromfile(file, dtype='>u2'))
    scans = np.asarray(scans)
    scans = scans[:, 300:-20]
    return np.asarray(np.stack(scans, axis=1))


def reconstruct_aScans(data_in: np.ndarray, dc_crop: int = 25, nd_filter: int = 3) -> np.ndarray:
    """ Performs SS-OCT reconstruction on array """
    # average stack
    stack = np.mean(data_in, axis=1)
    aLen = stack.shape[0]
    # windowing
    REC = OctReconstructionManager()
    stack = np.multiply(stack, REC.create_comp_disp_vec(
        aLen, (5, -30, 0, 0), 'Hann'))
    # abs of iFFT of padded array
    stack = np.abs(np.fft.ifft(
        np.pad(stack, (aLen, 0), mode='constant', constant_values=0)))
    # scale of first half of complex conjugate F^-1(signal) to 8Bit
    stack = 20 * np.log10(np.abs(stack[dc_crop:aLen]))
    ##snr = round(np.max(stack)-np.mean(stack[5000:11000]), 0) + (nd_filter*10)
    # return a-Scan scaled within dynamic range
    return np.asarray(stack)


def find_nearest_min_max_idx(array, value):
    array = np.asarray(array)
    idx_min = (np.abs(array - value)).argmin()
    idx_max = (np.abs(array + value)).argmax()
    return idx_min, idx_max


def run():
    IM = OctImport()
    all_raw_scans = []
    all_scans = []
    all_snrs = []
    files = glob.glob(os.path.join(IM._tk_folder_selection(), '*/'))
    for file in files:
        curr_scans = load_detector_signals(file)
        all_raw_scans.append(np.mean(curr_scans, axis=1))
        recon_scan, snr = reconstruct_aScans(curr_scans)
        all_scans.append(recon_scan)
        print(snr)
        all_snrs.append(snr)
    return np.asarray(all_scans), all_raw_scans, all_snrs


def high_low_envelopes_idxs(s, dmin=1, dmax=1, split=False):
    """
    TBD - does not work too good yet... Or at all
    """
    # locals min      
    lmin = (np.diff(np.sign(np.diff(s))) > 0).nonzero()[0] + 1 
    # locals max
    lmax = (np.diff(np.sign(np.diff(s))) < 0).nonzero()[0] + 1 
    if split:
        # s_mid is zero if s centered around x-axis or more generally mean of signal
        s_mid = np.mean(s) 
        # pre-sorting of locals min based on relative position with respect to s_mid 
        lmin = lmin[s[lmin]<s_mid]
        # pre-sorting of local max based on relative position with respect to s_mid 
        lmax = lmax[s[lmax]>s_mid]
    # global max of dmax-chunks of locals max 
    lmin = lmin[[i+np.argmin(s[lmin[i:i+dmin]]) for i in range(0,len(lmin),dmin)]]
    # global min of dmin-chunks of locals min 
    lmax = lmax[[i+np.argmax(s[lmax[i:i+dmax]]) for i in range(0,len(lmax),dmax)]]    
    return lmin,lmax


if __name__ == '__main__':
    path = r"C:\Users\PhilippsLabLaptop\Downloads\Signal"
    signal = load_detector_signals(path)
    mean_sig = np.mean(signal, axis=1)
    path = r"C:\Users\PhilippsLabLaptop\Downloads\Background"
    background = load_detector_signals(path)
    mean_bg = np.mean(background, axis=1)
    
    lmin_bg, lmax_bg = high_low_envelopes_idxs(mean_bg)
    lmin_sig, lmax_sig = high_low_envelopes_idxs(mean_sig)
    
    recon_sig = reconstruct_aScans(signal)
    recon_sig_bg_rm = reconstruct_aScans(signal-background)
    
    # # plot
    fig, ax = plt.subplots(3, 1)
    
    ax[0].plot(signal[:,0], label = 'First OCT Fringe Signal')
    ax[0].plot(mean_sig, label='Averaged OCT Fringe Signal')
    ax[0].plot(background[:,0], label='First OCT Background Signal')
    ax[0].plot(mean_bg, label='Averaged OCT Background Signal')
    ax[0].legend()

    ax[1].plot(mean_sig, label='Averaged OCT Fringe Signal')
    ax[1].plot(lmax_sig, mean_sig[lmax_sig], 'g', label='Maximum Envelope')
    ax[1].plot(lmin_sig, mean_sig[lmin_sig], 'r', label='Minimum Envelope')
    # # ax[1].plot(np.arange(mean_bg.shape[0]-1)[lmax], rec_raw[lmax], 'g', label='high')
    plt.show()


