import os
import cv2
import glob
import numpy as np
from tqdm.auto import tqdm
import matplotlib.pyplot as plt


def resize_volume(path_loading: str, in_dims: tuple, out_dims: tuple, noise_crop: float) -> np.array:
    with open(path_loading) as f:
        vol = np.fromfile(f, dtype=np.uint8).reshape(in_dims)
    out = np.zeros(out_dims)
    for i in range(vol.shape[-1]):
        out[...,i] = cv2.resize(vol[...,i], (out_dims[1],out_dims[0]))
    out = out-(noise_crop*out.max())
    out[out<0] = 0
    return out


def save_vol_2disk(vol: np.array, vol_path_loading: str) -> None:
    dims = vol.shape
    tail, head = os.path.split(vol_path_loading)
    pre_path = os.path.join(tail, 'Resized')
    if not os.path.isdir(pre_path):
        os.mkdir(pre_path)
    filename = os.path.join(pre_path, ''.join(head.split('_')[:-1]) + '_' + str(dims[0]) + 'x' + str(dims[1]) + 'x' + str(dims[2]) + '.bin')
    print(vol.shape)
    vol.astype(np.uint8).tofile(filename)


def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)


def average_volumes_from_list(vol_list: list, dims: tuple) -> np.array:
    out_vol = np.zeros((*dims,len(vol_list)), dtype=np.uint8)
    for i, vol in tqdm(enumerate(vol_list)):
        with open(vol) as f:
            out_vol[...,i] = np.fromfile(f, dtype=np.uint8).reshape(dims)
    return np.mean(out_vol, axis=-1)

def generate_enface_images(vol: np.array) -> np.array:
    pass
    # enface_stack

def calculate_snr_for_nVols(vol_list: list, dims: tuple) -> np.array:
    snr = []
    out_vol = np.zeros((*dims,len(vol_list)), dtype=np.uint8)
    for i, vol in tqdm(enumerate(vol_list)):
        with open(vol) as f:
            out_vol[...,i] = np.fromfile(f, dtype=np.uint8).reshape(dims)
    return np.mean(out_vol, axis=-1)
    

if __name__ == '__main__':
    a = [[1,2],[3,4]]
    print(a[1,1], a[1][1])
    # path_vol = r"C:\Users\phili\Desktop\20230221_110638_binaries\Resized"
    # file_paths = glob.glob(path_vol + '/*.bin')
    # v = average_volumes_from_list(file_paths, (403,391,391))
    # print(v.shape)
    # # fig, ax = plt.subplots(1,3)
    # # ax[0].imshow(v[:,:,200])
    # # ax[1].imshow(v[:,200,:])
    # # ax[2].imshow(np.mean(v, axis=0))
    # # plt.show()
    # v.astype(np.uint8).tofile(r"C:\Users\phili\Desktop\20230221_110638_binaries\Resized\100xAveraged_20230221_110843_403x391x391.bin")