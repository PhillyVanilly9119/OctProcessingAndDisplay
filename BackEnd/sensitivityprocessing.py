"""

@author:    Philipp
            philipp.matten@meduniwien.ac.at

@copyright: Medical University of Vienna,
            Center for Medical Physics and Biomedical Engineering

"""


import os
import sys
import glob
import numpy as np
import matplotlib.pyplot as plt

# custom imports 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Config')))

from octdatafilemanager import OctDataFileManager as OctImport
from octreconstructionmanager import OctReconstructionManager
from guiconfigdatamanager import ConfigDataManager 


def load_detector_signals(path: str, dtype: str='>u2', crop_range: tuple=(300,-20)) -> np.ndarray:
    """ Load all *.bin-files from path """
    files = glob.glob(os.path.join(path + "/*.bin"))
    scans = []
    for file in files:
        scans.append(np.fromfile(file, dtype=dtype))
    scans = np.asarray(scans)
    scans = scans[:, crop_range[0]:crop_range[1]]
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


def high_low_envelopes_idxs(s, dmin=1, dmax=1, split=True):
    """
    @param: 
    @return: 
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
    return lmin, lmax

# ------------------------------------------------------------------------------------------

def stack_all_scans_from_subdir(main_path: str, is_ret_avrgd_scans: bool=False) -> np.array:
    """  """
    def get_list_of_abs_file_paths(directory):
        """ @return: list of full path to all sub-dirs in directory """
        full_file_list = []
        for dirpath, dirnames, _ in os.walk(directory):
            for f in dirnames:
                full_file_list.append(os.path.join(dirpath, f))
        return full_file_list       
    assert os.path.isdir(main_path)
    full_file_list = get_list_of_abs_file_paths(main_path)
    stacked_data = []
    for folder in full_file_list:
        if is_ret_avrgd_scans:
            stacked_data.append(np.mean(load_detector_signals(folder), axis=-1))
        else :
            stacked_data.append(load_detector_signals(folder))
    return np.swapaxes(np.asarray(stacked_data), 0, 1)

#--------------------------------------------------------------------------------------------------------
def plot_all_scans_in_stack(data: np.array, title: str=None, x_label: str=None, y_label: str=None) -> None:
    """ WARNING: asserts data to have shape like 
    expected from stack_all_scans_from_subdir() !!! """
    fig = plt.figure()
    for scan in range(data.shape[1]):
        plt.plot(data[:,scan])
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
    return fig

#-------------------------------------------------------------
def crop_data_range(data: np.array, range: tuple) -> np.array:
    """ @return: A-scan cropped array, depending on range vals """
    assert len(range) == 2
    if range[0] == 0 and range[1] == 0: # both==0 -> full-range-of-array 
        return data[0:data.shape[0]]
    elif range[0] == 0 and range[1] != 0: #second==0 -> 0  till len(arr)//2
        return data[0:data.shape[0]//2]
    elif range[0] != 0 and range[1] == 0: # first==0 -> len(arr)//2 till end-of-array
        return data[data.shape[0]//2:data.shape[0]]
    else:
        return data[range[0]:range[1]] # none are 0 -> crop range
    
#-----------------------------------------------------------------------------
def plot_all_raw_data(main_path: str, is_ret_avrgd_scans: bool, aScan_range: tuple) -> None:
    """ Meant to visualize the plot in function body """
    data = stack_all_scans_from_subdir(main_path, is_ret_avrgd_scans=is_ret_avrgd_scans)
    data = crop_data_range(data, aScan_range)
    fig = plot_all_scans_in_stack(data, 
                                  title='Raw patterns (unprocessed OCT fringes)',
                                  x_label="Frequency Samples [a.u.]", 
                                  y_label="Relative signal strength [a.u. - samples]")
    plt.show()
    return

#-----------------------------------------------------------------------------
def plot_all_recon_data(main_path: str, aScan_range: tuple) -> None:
    """ Meant to visualize the plot in function body """
    data = stack_all_scans_from_subdir(main_path, is_ret_avrgd_scans=True)
    recon_data = []
    JSON = ConfigDataManager(filename='DefaultReconParams').load_json_file()
    REC = OctReconstructionManager()
    for scan in range(data.shape[1]):
        d3 = -15
        d2 = 4
        samples_dc_crop = 25
        recon_data.append(REC._run_reconstruction(data[:,scan], 
                                                  disp_coeffs = JSON['dispersion_coefficients'], 
                                                  wind_key = JSON['windowing_key'],
                                                  samples_hf_crop = JSON['hf_crop_samples'], 
                                                  samples_dc_crop = JSON['dc_crop_samples'],
                                                  blck_lvl = JSON['black_lvl_for_dis'], 
                                                  scale_fac = JSON['disp_scale_factor']
                                                  )
                          )
    recon_data = np.swapaxes(recon_data, 0, 1)
    data = crop_data_range(recon_data, aScan_range)
    # recon_data = recon_data[:,:10]
    fig = plot_all_scans_in_stack(recon_data, 
                                  title=f'Reconstructed OCT Signals (cropped DC samples = ({data.shape[0]-samples_dc_crop}/{data.shape[0]}))',
                                  x_label="Optical Depth [a.u.]", 
                                  y_label="Relative Signal Strength [dB (0-255)]")
    plt.show()
    return

def plot_2Ascans(sig_path1: str=r"C:\Users\PhilippsLabLaptop\Desktop\RollOff\01", 
                 sig_path2: str=r"C:\Users\PhilippsLabLaptop\Desktop\RollOff\23") :
    # load and pre-process OCT signal
    path1 = sig_path1
    assert os.path.isdir(path1)
    signal1 = load_detector_signals(path1)
    signal1 = signal1-np.mean(signal1, axis=0) # center around 0, for seemless dtype-conversion
    mean_sig1 = np.mean(signal1-np.mean(signal1, axis=0), axis=1)
    
    path2 = sig_path2
    assert os.path.isdir(path2)
    signal2 = load_detector_signals(path2)
    signal2 = signal2-np.mean(signal2, axis=0) # center around 0, for seemless dtype-conversion
    mean_sig2 = np.mean(signal2-np.mean(signal2, axis=0), axis=1)
         
    # reconstruct A-scans
    REC = OctReconstructionManager()
    d3 = -15
    d2 = 4
    d1, d0 = 0, 0
    
    recon_sig1 = REC._run_reconstruction(mean_sig1, (d3, d2, d1, d0),
                                         'Hann', samples_dc_crop=50,
                                         scale_fac=63.75, blck_lvl=85)
    recon_sig2 = REC._run_reconstruction(mean_sig2, (d3, d2, d1, d0),
                                         'Hann', samples_dc_crop=50,
                                         scale_fac=63.75, blck_lvl=85)
    
    def find_nearest(array, value) -> tuple:
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx], idx
    
    _, peak1 = find_nearest(recon_sig1, np.max(recon_sig1))
    _, half_fwhm1 = find_nearest(recon_sig1, np.max(recon_sig1)-3)
    fwhm1 = 2*np.abs(half_fwhm1-peak1)
    print(f"Peak position for scan 1: {peak1}, left most -3dB position: {half_fwhm1}, results in FWHM: {fwhm1}[pxls]")
    
    _, peak2 = find_nearest(recon_sig2, np.max(recon_sig2))
    _, half_fwhm2 = find_nearest(recon_sig2, np.max(recon_sig2)-3)
    fwhm2 = 2*np.abs(half_fwhm1-peak2)
    print(f"Peak position for scan 1: {peak2}, left most -3dB position: {half_fwhm2}, results in FWHM: {fwhm2}[pxls]")
    
    # plot
    print(mean_sig1.shape, mean_sig2.shape)
    fig, ax = plt.subplots(2, 1)
    ax[0].plot(signal1[:,0], label = 'OCT Fringe Signal')
    ax[0].plot(mean_sig1, label='Averaged 1st OCT Fringe Signal')
    ax[0].plot(signal2[:,0], label = 'OCT Fringe Signal')
    ax[0].plot(mean_sig2, label='Averaged 2nd OCT Fringe Signal')
    ax[0].legend(loc='lower left')
    # envelopes
    
    ax[1].plot(recon_sig1, label = 'OCT Fringe Signal No. 1')
    # ax[0,0].plot(mean_sig1, label='Averaged 1st OCT Fringe Signal')
    ax[1].plot(recon_sig2, label = 'OCT Fringe Signal No. 2')
    # ax[0,0].plot(mean_sig2, label='Averaged 1st OCT Fringe Signal')
    ax[1].legend(loc='lower left')    
    plt.show()
    

def plot_ascan_and_background(sig_path: str=r"C:\Users\PhilippsLabLaptop\Desktop\RollOff\01", 
                              bg_path: str=r"C:\Users\PhilippsLabLaptop\Desktop\RollOff\23") :
    # load and pre-process OCT signal
    path = sig_path
    assert os.path.isdir(path)
    signal = load_detector_signals(path)
    signal = signal-np.mean(signal, axis=0) # center arounf 0, for seemless dtype-conversion
    mean_sig = np.mean(signal-np.mean(signal, axis=0), axis=1)
    # load and pre-process BG signals
    path = bg_path
    if path is not None:
        assert os.path.isdir(path)
        background = load_detector_signals(path)
    else:
        background = np.zeros_like(signal)
    background = background-np.mean(background, axis=0) # center arounf 0, for seemless dtype-conversion
    mean_bg = np.mean(background-np.mean(background, axis=0), axis=1)
    
    lmin_sig, lmax_sig = high_low_envelopes_idxs(mean_sig, 5, 5, split=True)
    # lmin_bg, lmax_bg = high_low_envelopes_idxs(mean_bg, 5, 5, split=True)
    
    subbed_sig = np.subtract(signal[:,0], background[:,0], dtype=np.float32)
    subbed_mean_sig = np.subtract(mean_sig, mean_bg, dtype=np.float32)
        
    # reconstruct A-scans
    REC = OctReconstructionManager()
    d3 = -15
    d2 = 4
    d1, d0 = 0, 0
    
    subbed_recon_sig = REC._run_reconstruction(subbed_mean_sig, (d3, d2, d1, d0),
                                        'Hann', samples_dc_crop=50,
                                        scale_fac=63.75, blck_lvl=85)
    recon_sig = REC._run_reconstruction(mean_sig, (d3, d2, d1, d0),
                                        'Hann', samples_dc_crop=50,
                                        scale_fac=63.75, blck_lvl=85)
    
    def find_nearest(array, value) -> tuple:
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx], idx
    
    _, peak = find_nearest(recon_sig, np.max(recon_sig))
    _, half_fwhm = find_nearest(recon_sig, np.max(recon_sig)-3)
    fwhm = 2*np.abs(half_fwhm-peak)
    print(f"peak position: {peak}, left most -3dB position: {half_fwhm}, results in FWHM: {fwhm}[pxls]")
    
    # plot
    fig, ax = plt.subplots(2, 2)
    # raw data - SIG/BG single and averaged
    ax[0,0].plot(signal[:,0], label = 'OCT Fringe Signal')
    ax[0,0].plot(mean_sig, label='Averaged OCT Fringe Signal')
    ax[0,0].plot(background[:,0], label='OCT Background Signal')
    ax[0,0].plot(mean_bg, label='Averaged OCT Background Signal')
    ax[0,0].legend(loc='lower left')
    # envelopes
    ax[0,1].plot(mean_sig, label='Averaged OCT Fringe Signal')
    ax[0,1].plot(lmax_sig, mean_sig[lmax_sig], 'g', label='Maximum Envelope')
    ax[0,1].plot(lmin_sig, mean_sig[lmin_sig], 'r', label='Minimum Envelope')
    ax[0,1].legend(loc='lower left')
    # zoom-in on [0,0]
    ax[1,0].plot(signal[:recon_sig.shape[0]//50, 0] - np.mean(signal[:, 0]), label="OCT Fringe Signal")
    ax[1,0].plot(background[:recon_sig.shape[0]//50, 0] - np.mean(background[:, 0]), label="OCT Background Signal")
    ax[1,0].plot(subbed_sig[:recon_sig.shape[0]//50], label="OCT Fringe Signal - Background subtracted")
    ax[1,0].plot(subbed_mean_sig[:recon_sig.shape[0]//50], label="Background subtracted mean signal - mean(signal)-mean(background)")
    ax[1,0].legend(loc='lower left')
    
    ax[1,1].plot(recon_sig[:recon_sig.shape[0]//10], label=f"Reconstructed Averaged A-scan\n({d3},{d2},0,0) and a\nFWHM of {fwhm*1.1}µm [{fwhm}pxls]")  
    ax[1,1].plot(subbed_recon_sig[:1500], label=f"Reconstructed Averaged & BG-subbed A-scan\n({d3},{d2},0,0) and a\nFWHM of {fwhm*1.1}µm [{fwhm}pxls]")
    ax[1,1].legend(loc='upper left')
    
    plt.show()
      

if __name__ == '__main__':
    plot_all_recon_data(r'C:\Users\PhilippsLabLaptop\Desktop\RollOff\600kHz', aScan_range=(0, 0))
    
    # plot_ascan_and_background(sig_path=r"C:\Users\PhilippsLabLaptop\Downloads\Signal",
    #                           bg_path=r"C:\Users\PhilippsLabLaptop\Downloads\Background")
    # plot_2Ascans(sig_path1=r"C:\Users\PhilippsLabLaptop\Desktop\RollOff\100kHz\01",
    #              sig_path2=r"C:\Users\PhilippsLabLaptop\Desktop\RollOff\100kHz\23")