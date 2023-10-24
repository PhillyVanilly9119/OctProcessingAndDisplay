# %%
import cv2
import os, sys
import numpy as np
import matplotlib.pyplot as plt

# load remapping table
dtype_map_file = np.uint32
path_to_remapping_table = r"C:\Users\PhilippsLabLaptop\Desktop\04_Spiral_600_2_10.bin"
with open(path_to_remapping_table) as f:
    mapping_table = np.fromfile(f, dtype=dtype_map_file)

print(mapping_table)

# %%
