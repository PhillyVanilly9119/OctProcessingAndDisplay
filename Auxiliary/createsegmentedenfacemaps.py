import os
import glob 
import numpy as np
from PIL import Image
from tqdm import tqdm
from scipy import signal 
import matplotlib.image as image
import matplotlib.pyplot as plt


def load_volume(path: str, dims: tuple=(694, 391, 391)) -> np.array:
    with open(path, 'r') as f:
        vol = np.fromfile(f, dtype=np.uint8)
        return vol.reshape((dims))
    

def generate_enface_via_gradient_first_idx(vol: np.array, kernelsize: tuple=(1,1), offset: int=150) -> np.array:
    vol = signal.medfilt(vol, (3,3,3))
    if kernelsize == (1,1):
        kernelsize = (np.ceil(vol.shape[1])//2*2+1, np.ceil(vol.shape[2])//2*2+1)
    grad_vol = np.gradient(vol, axis=0)
    first_idxs = np.asarray(signal.medfilt(np.argmax(grad_vol, axis=0), (15,15)), dtype=np.uint16)
    enface = np.zeros((vol.shape[1], vol.shape[2]))
    for i in range(vol.shape[1]):
        for j in range(vol.shape[2]):
            enface[i,j] = np.asarray(np.mean(vol[first_idxs[i,j]+5:first_idxs[i,j]+offset, i, j], axis=0), dtype=np.uint8)
    enface = signal.medfilt(enface, (3,3))
    enface = (enface-np.min(enface))/(np.max(enface)-np.min(enface))
    return enface


def generate_enface_via_gradient_first_two_idxs(vol: np.array, kernelsize: tuple=(1,1)) -> np.array:
    vol = signal.medfilt(vol, (3,3,3))
    if kernelsize == (1,1):
        kernelsize = (np.ceil(vol.shape[1])//2*2+1, np.ceil(vol.shape[2])//2*2+1)
    grad_vol = np.gradient(vol, axis=0)
    first_idxs = np.asarray(signal.medfilt(np.argmax(grad_vol, axis=0), (15,15)), dtype=np.uint16)
    second_idxs = np.zeros((vol.shape[1], vol.shape[2]))
    for i in range(vol.shape[1]):
        for j in range(vol.shape[2]):
            second_idxs[i,j] = np.argmax(grad_vol[i, j, first_idxs[i,j]:])
    enface = np.zeros((vol.shape[1], vol.shape[2]))
    for i in range(vol.shape[1]):
        for j in range(vol.shape[2]):
            enface[i,j] = np.asarray(np.mean(vol[first_idxs[i,j]+5:second_idxs[i,j]-5, i, j], axis=0), dtype=np.uint8)
    enface = signal.medfilt(enface, (3,3))
    enface = (enface-np.min(enface))/(np.max(enface)-np.min(enface))
    return enface


def run():

    listings = [
        r"C:\Users\phili\Downloads\20240111_162642_binaries"
        ]

    for p_file in listings:
        glob_path = p_file #r"C:\Users\phili\Desktop\PhillyScripts\20230411_135910_Slammer1_binaries"
        file_paths = glob.glob(glob_path + "/*.bin")
        file_paths = [file for file in file_paths if "OctVolume" in file] 
        # print(file_paths) # debug
        dims=(644, 391, 391)

        volidx = []
        for i, file in tqdm(enumerate(file_paths)):
            vol = load_volume(file, dims)
            print(f"[INFO:] generating segmented en face map from {i} ({file})")
            enface = generate_enface_via_gradient_first_idx(vol)
            volidx.append(os.path.basename(file).split('.bin')[0]) 
            image.imsave(file.split('.bin')[0] + '.png', enface)
            

if __name__ == "__main__":
    run()

