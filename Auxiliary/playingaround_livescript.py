# %%
import os
import cv2
import sys
import glob
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
# %%

path = r"\\samba\p_Zeiss\Projects\4D OCT\Wetlabs\04_08_22_CowsEyes_OpenSky\Eye1\09_CowsEye1_ant\Reconstructed" 
files = glob.glob(path + "/*.bin")
images = []
for img in files:
    img = np.fromfile(img, dtype='<u1')
    img = np.reshape(img, (img.size//1024, 1024))
    img = cv2.resize(img, (2000, 4000))
    images.append(img)

images = np.asarray(images)
avg_scan = np.mean(images, axis=0)
print(images.shape, avg_scan.shape)

# fig, ax = plt.subplots(1,2, figsize=(20,20), dpi=450)
# ax[0].imshow(images[0,:,99:-101], cmap="gray")
# ax[0].axis('off')
# ax[1].imshow(avg_scan[:,99:-101], cmap="gray")
# ax[1].axis('off')
# plt.show()

fig, ax = plt.subplots(1,2, figsize=(20,20), dpi=450)
plt.imshow(images[0,:,99:-101], cmap="gray")
ax[0].axis('off')
ax[1].imshow(avg_scan[:,99:-101], cmap="gray")
ax[1].axis('off')
plt.show()

# safe_path = os.path.join(path, .split('.bin')[0] + '.png')
# %% Average recon scans and scale after averaging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'BackEnd')))
from octreconstructionmanager import OctReconstructionManager

path = r"D:\08042022_WetLabs\Eye1\01_CowsEye1_ant" 
files = glob.glob(path + "/*.bin")
raws = []
REC = OctReconstructionManager()

for img in tqdm(files):
    img = np.fromfile(img, dtype='<u2')
    img = np.reshape(img, (1024, img.size//1024))
    img = np.swapaxes(img, 1, 0)
    # plt.figure(figsize=(10,10), dpi=300)
    # plt.plot(img[:,1])
    # plt.show()
    # img = cv2.resize(img, (2000, 4000))
    img = REC._run_reconstruction_from_json(img, os.path.join(os.path.dirname( __file__ ), '..', 'Config', 'TestReconParams'))
    # plt.figure(figsize=(10,10), dpi=300)
    # plt.imshow(cv2.resize(img, (1000,2000)))
    # plt.show()
    raws.append(img)

raws = np.asarray(raws)
print(raws.shape)

black_level = 92
scale = 70

# single = np.mean(raws, axis=0)
single = np.asarray( 255 * ( (raws[0] - black_level) / scale ))
single[single < 0] = 0

plt.figure(figsize=(15,15), dpi=300)
plt.axis('off')
plt.imshow(cv2.resize(single, (1170,2800)), cmap='gray')
plt.show()

avg_scan = np.mean(raws, axis=0)
avg_scan = np.asarray( 255 * ( (avg_scan - black_level) / scale ))
avg_scan[avg_scan < 0] = 0

plt.figure(figsize=(15,15), dpi=300)
plt.axis('off')
plt.imshow(cv2.resize(avg_scan, (1170,2800)), cmap='gray')
plt.show()


# %%
b = 400
c = 400
a_new = 400
path = r"D:\08042022_WetLabs\Eye3" 
filename = "recon_rasterVol02_2_2000x400x400.bin"
full_file_name = os.path.join(path, filename)

volume = np.fromfile(full_file_name, dtype='<u1')
print(volume.shape, volume.size)
volume = np.reshape(volume, (b,volume.size//400//400,c))
print(volume.shape, volume.size)
o_vol = np.zeros((volume.shape[0], a_new, volume.shape[2]))
for bScan in tqdm(range(volume.shape[-1])):
    o_vol[:,:,bScan] = cv2.resize(volume[:,:,bScan], (a_new,400), interpolation=cv2.INTER_CUBIC)
volume = np.asarray(o_vol)
print(volume.shape, volume.size)
# p_min = 4000
# p_max = 6000
# # volume = volume[:,p_min:p_max,:]
# # print(volume.shape, volume.size)

# # a_len_new = 1600
# # new_a_lin_space = np.linspace(0, a_len_new, a_len_new+1, endpoint=True)
# # print(new_a_lin_space)
# # v_out = interp1d(volume, a_len_new, axis=1)

# filename_saving = r"D:\08042022_WetLabs\Eye2\recon_rasterVol03_3_" + str(p_max-p_min) + 'x' \
#     + str(volume.shape[0]) + 'x' + str(volume.shape[2]) + '.bin'
filename_saving = r"D:\08042022_WetLabs\Eye3\recon_rasterVol02_2_resized" + str(a_new) + 'x400x400' + '.bin'
# # # if not os.path.isfile(filename_saving):
# # #     os.mkdir(filename_saving)
volume.astype('<u1').tofile(filename_saving)

plt.figure(figsize=(20,20), dpi=300)
plt.imshow(volume[200,:,:])
plt.show()

# with open(filename_saving) as f:
# %%
import numpy as np
from scipy.interpolate import interp1d

ntime, nheight_in, nlat, nlon = (10, 20, 30, 40)

heights = np.linspace(0, 1, nheight_in)

t_in = np.random.normal(size=(ntime, nheight_in, nlat, nlon))
f_out = interp1d(heights, t_in, axis=1)

nheight_out = 50
new_heights = np.linspace(0, 1, nheight_out)
t_out = f_out(new_heights)


# %%
import os
import numpy as np
import matplotlib.pyplot as plt

a = 13312
b = 512
c = 512

main_path = "D:\\100kHz_RollOff"
file_path = "rasterVol01_13312x512x512_00.bin"
full_file_path = os.path.join(main_path, file_path)
print(full_file_path, os.path.isfile(full_file_path))

volume = np.fromfile(full_file_path, dtype='<u2')
print(volume.shape, volume.size)
volume = np.reshape(volume, (b, volume.size//b//c, c))
print(volume.shape, volume.size, a*b*c)
plt.imshow(volume[:,:,c//2])
plt.show()

# %%
## 03.06.2022 - reconstruction and visualization of axial resolution measurements
## C: @P.Matten
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'BackEnd')))

from octreconstructionmanager import OctReconstructionManager

path_signal = r"C:\Users\PhilippsLabLaptop\Desktop\RollOff\100kHz\exported_buffer_No.0_13312x1024.bin"
path_background = r"C:\Users\PhilippsLabLaptop\Desktop\RollOff\100kHz\exported_buffer_No.10_13312x1024.bin" 

b_signal = np.fromfile(path_signal, dtype=np.uint16)
b_background = np.fromfile(path_background, dtype=np.uint16)

b_signal = np.swapaxes(np.reshape(b_signal, (1024, 13312)), 0, 1)
b_background = np.swapaxes(np.reshape(b_background, (1024, 13312)), 0, 1)
print(b_signal.shape, b_background.shape)

b_signal_avg = np.mean(b_signal[:,:50], axis=-1)
b_background_avg = np.mean(b_background[:,:50], axis=-1)

REC = OctReconstructionManager()
rec_ = REC._run_reconstruction_from_json(np.array(b_signal, dtype=np.float32), 'DefaultReconParams')//4
rec_avg_ = REC._run_reconstruction_from_json(np.array(b_signal_avg-b_background_avg, dtype=np.float32), 'DefaultReconParams')//4

print(rec_.shape)
plt.figure(figsize=(15,15))
plt.plot(rec_[:2000,0])
plt.plot(rec_avg_[:2000])

def find_nearest(array, value) -> tuple:
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx], idx

_, peak = find_nearest(rec_avg_, np.max(rec_avg_))
_, half_fwhm = find_nearest(rec_avg_, np.max(rec_avg_)-3)
fwhm = 2*np.abs(half_fwhm-peak)
print(f"peak position: {peak}, left most -3dB position: {half_fwhm}, results in FWHM: {fwhm}[pxls]")

# %%
