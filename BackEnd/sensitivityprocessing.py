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

#---------------------------------------
def find_nearest(array, value) -> tuple:
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx], idx
    
#-----------------------------------------------------------------
def find_peak_and_fwhm(data: np.array, offset_db: int=3) -> tuple:
    _, peak = find_nearest(data, np.max(data))
    _, half_fwhm = find_nearest(data, np.max(data)-offset_db)
    fwhm = 2*np.abs(half_fwhm-peak)
    return peak, fwhm

#-------------------------------------------------------------------------------------------------
def load_detector_signals(path: str, dtype: str='>u2', crop_range: tuple=(300,-20)) -> np.ndarray:
    """ Load all *.bin-files from path """
    files = glob.glob(os.path.join(path + "/*.bin"))
    scans = []
    for file in files:
        scans.append(np.fromfile(file, dtype=dtype))
    scans = np.asarray(scans)
    scans = scans[:, crop_range[0]:crop_range[1]]
    return np.asarray(np.stack(scans, axis=1))

#-------------------------------------------
def find_nearest_min_max_idx(array, value):
    array = np.asarray(array)
    idx_min = (np.abs(array - value)).argmin()
    idx_max = (np.abs(array + value)).argmax()
    return idx_min, idx_max

#----------------------------------------------------------
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

#----------------------------------------------------------------------------------------------------------
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

#------------------------
# TODO: continue here
    

def plot_ascan_and_background(sig_path: str=r"C:\Users\PhilippsLabLaptop\Downloads\Signal", 
                              bg_path: str=r"C:\Users\PhilippsLabLaptop\Downloads\Background") :
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
    JSON = ConfigDataManager(filename='DefaultReconParams').load_json_file()
    subbed_recon_sig = REC._run_reconstruction(subbed_mean_sig, 
                                               disp_coeffs = JSON['dispersion_coefficients'], 
                                               wind_key = JSON['windowing_key'],
                                               samples_hf_crop = JSON['hf_crop_samples'], 
                                               samples_dc_crop = JSON['dc_crop_samples'],
                                               blck_lvl = JSON['black_lvl_for_dis'], 
                                               scale_fac = JSON['disp_scale_factor']
                                               )
    recon_sig = REC._run_reconstruction(mean_sig, 
                                        disp_coeffs = JSON['dispersion_coefficients'], 
                                        wind_key = JSON['windowing_key'],
                                        samples_hf_crop = JSON['hf_crop_samples'], 
                                        samples_dc_crop = JSON['dc_crop_samples'],
                                        blck_lvl = JSON['black_lvl_for_dis'], 
                                        scale_fac = JSON['disp_scale_factor']
                                        )
    
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
    ax[0,0].plot(lmax_sig, mean_sig[lmax_sig], 'deeppink', label='Maximum Envelope', linewidth=3)
    ax[0,0].plot(lmin_sig, mean_sig[lmin_sig], 'lawngreen', label='Minimum Envelope', linewidth=3)
    ax[0,0].legend(loc='lower left')
    ax[0,0].set_title("OCT raw fringes")
    # envelopes
    ax[0,1].plot(recon_sig, label=f"Reconstructed Averaged A-scan")  
    ax[0,1].plot(subbed_recon_sig, label=f"Reconstructed Averaged & BG-subbed A-scan")
    ax[0,1].legend(loc="upper right")
    ax[0,1].set_title("Reconstructed Averged A-scans")
    # zoom-in on fringes
    ax[1,0].plot(signal[:signal.shape[0]//50, 0] - np.mean(signal[:, 0]), label="OCT Fringe Signal")
    ax[1,0].plot(background[:background.shape[0]//50, 0] - np.mean(background[:, 0]), label="OCT Background Signal")
    ax[1,0].plot(subbed_sig[:subbed_sig.shape[0]//50], label="OCT Fringe Signal - Background subtracted")
    ax[1,0].plot(subbed_mean_sig[:subbed_mean_sig.shape[0]//50], label="Background subtracted mean signal - mean(signal)-mean(background)")
    ax[1,0].legend(loc='lower left')
    ax[1,0].set_title("Zoom-in on OCT raw fringes")
    # zoom-in on rconstructed signal
    ax[1,1].plot(recon_sig[:recon_sig.shape[0]//10], label=f"Reconstructed Averaged A-scan\n({JSON['dispersion_coefficients']}) and a FWHM of\n{fwhm*1.1}µm [{fwhm}pxls] (air -> n=1)\n({round(fwhm*1.1/1.36, 2)}µm (tissue -> n=1.36)")  
    ax[1,1].plot(subbed_recon_sig[:1500], label=f"Reconstructed Averaged & BG-subbed A-scan\n({JSON['dispersion_coefficients']}) and a FWHM of\n{fwhm*1.1}µm [{fwhm}pxls] (air -> n=1)\n({round(fwhm*1.1/1.36, 2)}µm (tissue -> n=1.36)")
    ax[1,1].legend(loc='upper left')
    ax[1,1].set_title("Zoom-in on Reconstructed Averged A-scans with Axial Resolution")
    
    plt.show()
      

if __name__ == '__main__':
    plot_all_recon_data(r'C:\Users\PhilippsLabLaptop\Desktop\RollOff\100kHz', aScan_range=(0, 0))
    # plot_ascan_and_background(sig_path=r"C:\Users\PhilippsLabLaptop\Desktop\RollOff\600kHz\01", 
    #                           bg_path=None)
    # plot_ascan_and_background()
