import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

recon_path = r"C:\Users\PhilippsLabLaptop\Documents\Programming\Repositories\OctProcessingAndDisplay\BackEnd\octreconstructionmanager.py"
sys.path.append(os.path.abspath(os.path.dirname(recon_path)))
from octreconstructionmanager import OctReconstructionManager

a_size = 13312

path_to_file = r"\\samba\p_Zeiss_Lab\Projects\4D OCT Engine\Data\20220308_WetLabs_IOLData\RasterCaptureScans\rasterVol03_13312x512x512.bin"
with open(path_to_file) as f:
    a_scan = np.fromfile(f, count=a_size, offset=a_size*255*255, dtype=np.uint16)

def find_closest_indices(arr, target_value):
    if not isinstance(arr, np.ndarray) or arr.ndim != 1:
        raise ValueError("Input must be a 1D NumPy array.")
    target_value = float(target_value)  # Convert to float for better precision
    absolute_diff = np.abs(arr - target_value)
    closest_indices = np.where(absolute_diff == absolute_diff.min())[0]
    
    return closest_indices
   
def gaussian(x, mean, std_dev):
    return np.exp(-(x - mean) ** 2 / (2 * std_dev ** 2)) / (std_dev * np.sqrt(2 * np.pi))

def gaussian_approximation_mse(data, mean, std_dev):
    if not isinstance(data, np.ndarray):
        raise ValueError("Input data must be a NumPy array.")
    x = np.arange(len(data))  # Create x-axis values for the Gaussian curve
    # Calculate the Gaussian curve with the given mean and standard deviation
    gaussian_curve = gaussian(x, mean, std_dev)
    # Calculate the Mean Squared Error (MSE)
    mse = np.mean((data - gaussian_curve) ** 2)
    return mse

 
# two ways to optimize:
# i) (optimal) assuming the data from which we reconstruct contains only a single-scatterer
# ii) finding n peaks to minitor the boradending of the PSF/FWHM
map = np.zeros((400, 400)) 
REC = OctReconstructionManager()
for c3 in range(-200, 200, 10):
    for c2 in range(-200, 200, 10):
        buffer = REC._run_reconstruction(a_scan, disp_coeffs=(c3, c2, 0, 0), wind_key="hann", blck_lvl=100, samples_dc_crop=50) 
        # 1. find a robost (set of) peak(s) for tracking PSF/FWHM
        offset = 10
        roi = (buffer.shape[0]//10, 4*buffer.shape[0]//10)
        peak_pos = np.unravel_index(np.argmax(buffer[roi[0]:roi[1], ...]), buffer.shape)[0]
        peak_min_range, peak_max_range = peak_pos-offset, peak_pos+offset
        buffer_in_peak_range = buffer[peak_min_range:peak_max_range]
        print(gaussian_approximation_mse(buffer[peak_pos-offset:peak_pos+offset], 0, 1))
        x = np.linspace(peak_min_range, peak_max_range, buffer_in_peak_range.shape[0])
        spline = UnivariateSpline(x, buffer_in_peak_range-np.max(buffer_in_peak_range)/2, s=0)
        r = spline.roots() # find the roots
        if len(r) >= 2:
            r1, r2 = int(r[0]), int(r[-1])
            plt.plot(buffer[r1:r2])
            plt.show()
            # print(buffer[peak_pos], buffer[r1], buffer[r2])
        # map[i,j] =
    

# plt.plot(np.abs(np.fft.fft(a_scan)))
# plt.show()
