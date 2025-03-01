import os
import cv2
import glob
import numpy as np 
from PIL import Image
from tqdm import tqdm
from PIL import Image
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from scipy.ndimage import median_filter


def find_files_via_file_strings(directory: str, search_substring: str, file_type: str):
    """
    Find all '.bin' files in a directory that contain a specific string in their names.
    """
    pattern = os.path.join(directory, '**', f'*{search_substring}*{file_type}')
    # Use glob to find matching files recursively
    return glob.glob(pattern, recursive=True)

def process_large_volumes(file_path: str, raw_dims: tuple) -> np.ndarray:
    """
    Process large volumes of data for reconstruction.

    Args:
        file_path: The file path of the input data.
        raw_dims: A tuple specifying the dimensions of the raw data.

    Returns:
        None
    """
    # Pre-allocations and sanity checks for function params
    a, b, c = raw_dims
    aLen_recon = 2700
    raw_bScan_file_size = a * b # B-scan size in voxels
    
    poly = np.asarray( np.polyval( (-5,125,0,0), np.linspace(-0.5, 0.5, a) ) )
    wind = np.asarray( np.hanning(a), dtype=np.float32 )
    x = np.multiply( poly, wind )
    y = np.multiply( np.cos( poly ), wind )
    dispersion = np.asarray( x + 1j * y, dtype=np.complex64 )

    file_saving = os.path.join(os.path.dirname(file_path), f"{os.path.basename(file_path).split('_')[0]}_{aLen_recon}x{b}x{c}_recon.bin")
    
    for n in tqdm(range(c)): # loop through "slow-scanning axis" for less-memory demanding reconstruction
        with open(file_path, 'rb') as f_raw:
            offset = n * raw_bScan_file_size * np.dtype(np.uint16).itemsize # pointer-offset in bytes
            raw_buffer = np.fromfile(f_raw, dtype=np.uint16, count=raw_bScan_file_size, offset=offset) 
            raw_buffer = np.reshape(raw_buffer, (b, a)).swapaxes(0,1) # reshape to size len(A-Scan) * len(B-Scan)
            raw_buffer = raw_buffer - np.mean(raw_buffer, axis=1)[:,np.newaxis] # BG subtraction
            raw_buffer = np.asarray(raw_buffer, dtype=np.complex64) # recast as complex array
            fft_buffer = np.zeros((2*a,b), dtype=np.complex64)
            fft_buffer[a:,:] = raw_buffer * dispersion[:,np.newaxis]
            buffer = 20 * np.log10( np.abs( np.fft.fft( fft_buffer, axis=0 )[:a] ) ) 
            buffer = 4 * (buffer - 90)
            buffer = np.clip(buffer, 0, 255).astype(np.uint8)
            buffer = buffer[100:2800,:]
            with open(file_saving, 'a+b') as f: 
                buffer.astype(np.uint8).tofile(f) # save cropped buffer in cropped version
    return 

def find_most_prominent_peaks(array, min_peak_width):
    """
    Finds the top peak in an array with the smallest index.

    Args:
        array: A list or array-like object containing numeric values.
        min_peak_width: An integer specifying the minimum width of a peak.

    Returns:
        A tuple containing the index and height of the top peak in the array.
        If no peaks are found, returns (None, None).

    """    
    peaks, _ = find_peaks(array, width=min_peak_width)
    if sorted_peaks := sorted(peaks, key=lambda x: array[x], reverse=True):
        top_peak = min(sorted_peaks[:3])
        bottom_peak = max(sorted_peaks[:3])
        return top_peak, bottom_peak
    else:
        return None, None
    
def save_depth_map(path: str, file_prefix: str, array: np.ndarray) -> None:
    """
    Saves a depth overlay image with a highlighted center point.

    Args:
        path: The file path to save the image.
        file_prefix: The prefix to use for the saved file.
        array: The NumPy array representing the image data.

    Returns:
        None
    """
    plt.imshow(array)
    # plt.scatter(tuple[1], tuple[0])
    plt.axis("off")
    path_epi_saving = os.path.join(os.path.dirname(path), f"{file_prefix}_{os.path.basename(path)[:-4]}.png")
    plt.savefig(path_epi_saving, bbox_inches='tight', pad_inches=0)

def overlay_images_with_alpha(img1: np.ndarray, img2: np.ndarray, alpha: float) -> np.ndarray:
    """
    Overlay two images with alpha blending.

    Args:
        img1: The first image as a NumPy array.
        img2: The second image as a NumPy array.
        alpha: The alpha value for blending the images.

    Returns:
        The overlayed image as a NumPy array.
    """
    result = (1 - alpha) * img1 + alpha * img2
    return np.clip(result, 0, 255).astype(np.uint8)

def overlay_vol_and_mask(vol_path: str, mask_path: str) -> np.ndarray:

    vol = np.fromfile(vol_path, dtype=np.uint8).reshape(700, 2700, 700).swapaxes(0,1) 
    mask = np.fromfile(mask_path, dtype=np.uint8).reshape(2700, 700, 700) 
    overlay_slice1 = overlay_images_with_alpha(vol[:,350,:], mask[:,350,:], alpha=0.5)
    overlay_slice2 = overlay_images_with_alpha(vol[:,:,350], mask[:,:,350], alpha=0.5)
    fig, ax = plt.subplots(1,2)
    ax[0].imshow(vol[:,350,:])
    ax[1].imshow(mask[:,350,:])
    plt.show()

def segment_interfaces_and_save_data(file: str) -> None:
    
    ## Pipeline for processing in batches
    # 1) load file
    vol = np.fromfile(file, dtype=np.uint8).reshape(700, 2700, 700).swapaxes(0,1)  
    
    # 2) allocate maps and mask
    epithelium = np.zeros((vol.shape[1], vol.shape[2]))
    endothelium = np.zeros((vol.shape[1], vol.shape[2]))
    cornea_mask = np.zeros(vol.shape, dtype=np.bool_)
    cornea_min_thickness = 100
    
    # 3) loop through A-scans and find indices of epithelium and endothelium 
    for x in tqdm(range(vol.shape[1])):
        for y in range(vol.shape[2]):
            p_1, _ = find_most_prominent_peaks(vol[:,x,y], min_peak_width=3)
            epithelium[x,y] = p_1
            _, p_2 = find_most_prominent_peaks(vol[p_1+cornea_min_thickness : p_1+4*cornea_min_thickness, x, y], min_peak_width=3)
            p_2 = p_2 + p_1 + cornea_min_thickness # add offsets to store true index in vol[a_scan_axis,...] 
            endothelium[x,y] = p_2

    # 4) filter for more robust detection of cornea tip
    epithelium = np.asarray(median_filter(epithelium, (21,21)), dtype=np.uint16)
    epithelium.astype(np.uint16).tofile(r"P:\Frankeneye\24\PBSt\epithelium_index_map_01_700x700_recon.npy")
    endothelium = np.asarray(median_filter(endothelium, (21,21)), dtype=np.uint16)
    endothelium.astype(np.uint16).tofile(r"P:\Frankeneye\24\PBSt\endothelium_index_map_01_700x700_recon.npy")

    epithelium[epithelium > 600] = 0
    endothelium[endothelium > 750] = 0

    def exponential_function(x, a, b):
        return a * np.exp(b * x)

    # 4.1.1)
    mean_map = np.zeros((700,700))
    for x in tqdm(range(vol.shape[1])):
        for y in range(vol.shape[2]):
            d_range = vol[epithelium[x,y]:endothelium[x,y],x,y]
            if len(d_range) > 0:
                try:
                    params, covariance = curve_fit(exponential_function, np.linspace(1, len(d_range)+1, len(d_range)), d_range)
                    mean_map[x,y] = params[0]
                except RuntimeError as e:
                    # Handle the exception here
                    print(f"Error: {e}")
                    params = [1, 1]
                    covariance = None
    
    fig, ax = plt.subplots()
    im = ax.imshow(mean_map, cmap='viridis')
    cbar = plt.colorbar(im)
    cbar.set_ticks([-1e-12, 1e-12])  # Set tick positions
    caption_text = "Normalized intensities [n.n. a.u.]"
    caption_fontsize = 15
    cbar.ax.text(1.1, 0.5, caption_text, va='center', rotation='vertical', fontsize=caption_fontsize)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()

    # # 4.1) apply filtered masks as GT for mask creation
    # for x in tqdm(range(vol.shape[1])):
    #     for y in range(vol.shape[2]):        
    #         cornea_mask[p_1+5:p_2-5, x, y] = 1
    
    # print(f"[INFO:] Mean thickness on epithelium in {file} is {np.mean(epithelium, axis=None)} and of the endothelium {np.mean(endothelium, axis=None)}")
    # # find tip of cornea for centering purposes and save overlays of depth maps to disk
    # print( np.unravel_index(np.argmin(epithelium), epithelium.shape) )
    # save_depth_map(file, "epithelium_pixel_map", epithelium)
    # print( np.unravel_index(np.argmin(endothelium), endothelium.shape) )
    # save_depth_map(file, "endothelium_pixel_map", endothelium)
    
    # # 5) save mask to disk
    # mask_file = os.path.join(os.path.dirname(file), f"cornea_mask_{os.path.basename(file)[:-4]}.npy")
    # cornea_mask.astype(np.bool_).tofile(mask_file)

def load_layer_and_vol_data(p_vol, p_epithelium, p_endothelium):
    vol = np.fromfile(p_vol, dtype=np.uint8).reshape(700, 2700, 700).swapaxes(0,1)
    epithelium = cv2.cvtColor(np.array(Image.open(p_epithelium)), cv2.COLOR_RGB2GRAY)
    endothelium = cv2.cvtColor(np.array(Image.open(p_endothelium)), cv2.COLOR_RGB2GRAY)
    return vol, epithelium, endothelium

def run():

    main_dir = r"P:\Frankeneye\48"
    string = 'recon'
    segment_interfaces_and_save_data(r"P:\Frankeneye\24\PBSt\01_2700x700x700_recon.bin")
    # p_epi = r"P:\Frankeneye\24\PBSt\epithelium_pixel_map_01_2700x700x700_recon.png"
    # p_endo = r"P:\Frankeneye\24\PBSt\endothelium_pixel_map_01_2700x700x700_recon.png"
    # p_vol = r"P:\Frankeneye\24\PBSt\01_2700x700x700_recon.bin"
    # v, epi, endo = load_layer_and_vol_data(p_vol, p_epi, p_endo)
    # print(v.shape, endo.shape, epi.shape)
    # plt.imshow(epi, cmap="gray")
    # plt.show()

if __name__ == "__main__":
    run()
