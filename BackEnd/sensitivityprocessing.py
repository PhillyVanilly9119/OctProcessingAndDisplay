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
    files = glob.glob(os.path.join(path + "/*.bin"))
    scans = []
    for file in files :
        scans.append(np.fromfile(file, dtype='>u2'))
    scans = np.asarray(scans)
    scans = scans[:,300:-20] 
    return np.asarray(np.stack(scans, axis=1))


def reconstruct_aScans(data_in: np.ndarray, dc_crop: int=25, nd_filter: int=3) -> np.ndarray:
    """ Performs SS-OCT reconstruction on array """
    # average stack
    stack = np.mean(data_in, axis=1)
    aLen = stack.shape[0]
    # windowing
    stack = np.multiply( stack, np.hanning(aLen) )
    # abs of iFFT of padded array
    stack = np.abs( np.fft.ifft( np.pad( stack, (aLen, 0), mode='constant', constant_values=0 ) ) )
    # scale of first half of complex conjugate F^-1(signal) to 8Bit 
    stack = 20 * np.log10( np.abs(stack[dc_crop:aLen]) )
    snr = round(np.max(stack)-np.mean(stack[5000:11000]), 0) + (nd_filter*10)
    # return a-Scan scaled within dynamic range 
    return np.asarray(stack), snr

def plot_aScan():
    """TBD"""
    pass

def plot_aScans():
    """TBD"""
    pass

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


if __name__ == '__main__':
    scans, raw_scans, snrs = run()
    power_vector = [2.5,250,500,750,1000,1250,1500,1750]
    
    plot1 = plt.figure(1, figsize=(8, 4.5), dpi=300)
    plt.title(f"Reconstructed A-scans w/ SNRs -- {snrs}", fontsize=10)
    ax1 = plt.plot(np.transpose(scans))
    plt.xlabel("Samples [n]")
    plt.ylabel("Signal in relative units [dB]")
    plt.savefig(r'C:\Users\Philipp\Desktop\SignalPlot.png')
    
    # plot2 = plt.figure(2, figsize=(8, 4.5), dpi=300)
    # # ax2 = plt.plot(power_vector, snrs)
    # ax2 = plt.plot(snrs)
    # ax2.set_ylim([0, 120])
    # plt.title("SNR as function of reference arm power")
    # plt.xlabel("Reference arm power [uW]")
    # plt.ylabel("Sensitivity [dB]")
    # plt.savefig(r'C:\Users\Philipp\Desktop\SensitivityPlot.png')
    
    plot10 = plt.figure(10, figsize=(8, 4.5), dpi=300)
    plt.title("Raw A-scans", fontsize=10)
    ax1 = plt.plot(np.transpose(raw_scans))
    plt.xlabel("Samples [n]")
    plt.ylabel("Signal in relative units [a.u.]")
    plt.savefig(r'C:\Users\Philipp\Desktop\RawSignalPlot.png')

