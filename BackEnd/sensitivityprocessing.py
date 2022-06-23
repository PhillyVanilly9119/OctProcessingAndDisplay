"""

@author:    Philipp
            philipp.matten@meduniwien.ac.at

@copyright: Medical University of Vienna,
            Center for Medical Physics and Biomedical Engineering

"""


import os
import cv2
import sys
import glob
import time
import numpy as np
import matplotlib.pyplot as plt

# custom imports 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Config')))

from octdatafilemanager import OctDataFileManager as OctImport
from octreconstructionmanager import OctReconstructionManager
from configdatamanager import ConfigDataManager 

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

#------------------------------------------------
def load_uncropped_aScans(path: str, shape: tuple, dtype: str='<u2') -> np.array:
    """  """
    all_files = glob.glob(path + "/*.bin")
    data_stack = []
    for file in all_files:
        data_block = np.fromfile(file, dtype=dtype)
        data_block = np.reshape(np.asarray(data_block), shape)
        background = np.array(np.mean(data_block, axis=-1), dtype=np.float32)
        aScan = np.array(data_block[:, data_block.shape[1]//2], np.float32)
        np.subtract(aScan, background, dtype=np.float32)
        data_stack.append(np.subtract(aScan, background, dtype=np.float32))
    return np.asarray(data_stack)

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
def plot_all_recon_data(data: np.array, aScan_range: tuple) -> None:
    """ Meant to visualize the plot in function body """
    recon_data = []
    REC = OctReconstructionManager()
    for scan in range(data.shape[1]):
        recon_scan = REC._run_reconstruction_from_json(data[:,scan], 'DefaultReconParams')
        recon_data.append(recon_scan)
    recon_data = np.swapaxes(recon_data, 0, 1)
    data = crop_data_range(recon_data, aScan_range)
    JSON = ConfigDataManager(filename='DefaultReconParams').load_json_file()
    dc_crop = JSON['dc_crop_samples']
    fig = plot_all_scans_in_stack(recon_data, 
                                  title=f'Reconstructed OCT Signals (cropped DC samples = ({data.shape[0]-dc_crop}/{data.shape[0]}))',
                                  x_label="Optical Depth [a.u.]", 
                                  y_label="Relative Signal Strength [uint8-range-mapped (0-255)]"
                                  )
    plt.show()
    return recon_data

#----------------------------------------------------------------------------------------------------------
def plot_enfaces(data: np.array, aScan_range: tuple, img_name: str='', json_file_name: str="DefaultReconParams", 
                 is_save_img: bool=False, is_save_data: bool=False) -> np.array:
    """ Visualiazes the en face images of a raw and the corresponding reconstructed volume"""
    REC = OctReconstructionManager()
    print("[INFO:] Generating raw en face...")
    raw_enface = np.mean(data, axis=0)
    print("[INFO:] Done!")
    print("[INFO:] Reconstructing entire OCT volume (this may take some time...)")
    t1 = time.perf_counter()
    recon_data = REC._run_reconstruction_from_json(data, json_file_name)
    print(f"[INFO:] Done! (Took {round(time.perf_counter()-t1,2)} secs)")
    print("[INFO:] Generating en face from reconstructed volume...")
    recon_enface = np.mean(recon_data[200:], axis=0)
    print("[INFO:] Done!")
    
    recon_maxes = np.squeeze(np.argwhere(recon_enface.max() == recon_enface))
    raw_mins = np.squeeze(np.argwhere(raw_enface.min() == raw_enface))
    # print( recon_maxes[0], raw_mins[0], int(np.floor( (recon_maxes[0]+raw_mins[0])//2)) )
    pxl_offset = 2
    x_centroid = int(recon_maxes[1])
    y_centroid = int(recon_maxes[0])
    print(x_centroid, y_centroid)
    if x_centroid % data.shape[1] <= pxl_offset:
        x_centroid = x_centroid - (x_centroid % data.shape[1])
    if y_centroid % data.shape[2] <= pxl_offset:
        y_centroid = y_centroid - (y_centroid % data.shape[2])
    print(x_centroid, y_centroid)
    
    # --- Plotting ---
    fig, ax = plt.subplots(1,4, figsize=(19.2,10.8), dpi=100)
    ax[0].imshow(raw_enface, cmap='gray')
    ax[0].axis('off')
    ax[0].set_title("Raw ENFACE")
    
    ax[1].imshow(recon_enface, cmap='gray')
    circle = plt.Circle((x_centroid, y_centroid), pxl_offset, color='b')
    ax[1].add_patch(circle)
    ax[1].axis('off')
    ax[1].set_title("Recon ENFACE")
    
    ax[2].imshow(cv2.resize(np.mean(recon_data[:,x_centroid-pxl_offset:x_centroid+pxl_offset,:], axis=1), (1000,2000)), cmap='gray')
    ax[2].axis('off')
    ax[2].set_title("Middle B-scan (X-Centroid) of reconstructed volume")
     
    ax[3].imshow(cv2.resize(np.mean(recon_data[:,:,y_centroid-pxl_offset:y_centroid+pxl_offset], axis=2), (1000,2000)), cmap='gray')
    ax[3].axis('off')
    ax[3].set_title("Middle B-scan (Y-Centroid) of reconstructed volume")
    
    plt.show()
    
    # --- Post-Processing ---
    print(f"Saving A-scans with indices: X = {x_centroid-1} to {x_centroid+1} and Y = {y_centroid-1} to {y_centroid+1}")
    if is_save_img:
        plt.savefig(img_name)
    if is_save_data:
        data[:, x_centroid-pxl_offset:x_centroid+pxl_offset, y_centroid-pxl_offset:y_centroid+pxl_offset].astype('<u2').tofile(img_name.split('.png')[0] + '.bin')

    
#---------------------------------------------------------------------------------------------
def plot_ascan_and_background(sig_path: str=r"C:\Users\PhilippsLabLaptop\Downloads\Signal", 
                              bg_path: str=r"C:\Users\PhilippsLabLaptop\Downloads\Background",
                              diff_2fwhm: int=12, pixel_pitch: float=2.84) :
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
    subbed_recon_sig = REC._run_reconstruction_from_json(subbed_mean_sig, 'DefaultReconParams')
    recon_sig = REC._run_reconstruction_from_json(mean_sig, 'DefaultReconParams')
    
    def find_nearest(array, value) -> tuple:
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx], idx
    
    _, peak = find_nearest(recon_sig, np.max(recon_sig))
    _, half_fwhm = find_nearest(recon_sig, np.max(recon_sig)-diff_2fwhm)
    fwhm = 2*np.abs(half_fwhm-peak)
    print(f"peak position: {peak}, left most -3dB position: {half_fwhm}, results in FWHM: {fwhm}[pxls]")
    
    # --- Plot ---
    JSON = ConfigDataManager('DefaultReconParams').load_json_file() 
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
    ax[0,1].plot(recon_sig, label="Reconstructed Averaged A-scan")  
    ax[0,1].plot(subbed_recon_sig, label="Reconstructed Averaged & BG-subbed A-scan")
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
    ax[1,1].plot(recon_sig[:recon_sig.shape[0]//10], label=f"Reconstructed Averaged A-scan\n({JSON['dispersion_coefficients']}) and a FWHM of\n{round(fwhm*pixel_pitch, 2)}µm [{fwhm}pxls] (air -> n=1)\n({round(fwhm*pixel_pitch/1.36, 2)}µm (tissue -> n=1.36)")  
    ax[1,1].plot(subbed_recon_sig[:1500], label=f"Reconstructed Averaged & BG-subbed A-scan\n({JSON['dispersion_coefficients']}) and a FWHM of\n{round(fwhm*pixel_pitch, 2)}µm [{fwhm}pxls] (air -> n=1)\n({round(fwhm*pixel_pitch/1.36, 2)}µm (tissue -> n=1.36)")
    ax[1,1].legend(loc='upper left')
    ax[1,1].set_title("Zoom-in on Reconstructed Averged A-scans with Axial Resolution")
    # show all subplots
    plt.show()
      

def run() -> None:
    """ main function if script is executed by interpreter """
    print("[Info:] Running from    < sensitivityprocessing.py >    ... ")
    plot_ascan_and_background(sig_path=r"\\samba\p_Zeiss\Publications\Journal Publications\4D OCT Engine\AuxiliaryData\AxialResolution\Signal",
                              bg_path=r"\\samba\p_Zeiss\Publications\Journal Publications\4D OCT Engine\AuxiliaryData\AxialResolution\Background")
    # data = load_detector_signals(r"\\samba\p_Zeiss\Publications\Journal Publications\4D OCT Engine\AuxiliaryData\AxialResolution\ref")
    # plot_all_recon_data(data, (0,0))

if __name__ == '__main__':
    run()
 