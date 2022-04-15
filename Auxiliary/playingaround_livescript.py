# %%
from audioop import avg
import cv2
import glob
import os, sys
import numpy as np
import matplotlib.pyplot as plt
# %%

path = r"D:\08042022_WetLabs\01_CowsEye1_ant\Reconstructed" 
files = glob.glob(path + "/*.bin")
images = []
for img in files:
    img = np.fromfile(img, dtype='<u1')
    img = np.reshape(img, (img.size//1024, 1024))
    img = cv2.resize(img, (1500, 3000))
    images.append(img)

images = np.asarray(images)
avg_scan = np.mean(images, axis=0)

fig, ax = plt.subplots(1,2, figsize=(20,20), dpi=300)
ax[0].imshow(images[0], cmap="gray")
ax[0].axis('off')
ax[1].imshow(avg_scan, cmap="gray")
ax[1].axis('off')
plt.show

# safe_path = os.path.join(path, .split('.bin')[0] + '.png')

# %%
