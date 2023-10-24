

import os
import sys
import json
import glob
import numpy as np
import pandas as pd


files_test_data = r"C:\Users\PhilippsLabLaptop\Desktop\BenData\test_data\diabetic"
files_training_data = r"C:\Users\PhilippsLabLaptop\Desktop\BenData\training_data\diabetic"

combined_diabetic_list = glob.glob(files_test_data + "./*.png") + glob.glob(files_training_data + "./*.png")
file_ids_diabetic = [os.path.basename(file).split('x2_')[-1].split('.png')[0] for file in combined_diabetic_list]

files_test_data = r"C:\Users\PhilippsLabLaptop\Desktop\BenData\test_data\healthy"
files_training_data = r"C:\Users\PhilippsLabLaptop\Desktop\BenData\training_data\healthy"

combined_healthy_list = glob.glob(files_test_data + "./*.png") + glob.glob(files_training_data + "./*.png")
file_ids_healthy = [os.path.basename(file).split('x2_')[-1].split('.png')[0] for file in combined_healthy_list]


rootdir = r"\\samba\p_Zeiss_clin\Projects\UWF_OCTA\Clinical_data\MOON1\02 Diabetes"
database_patient_files = []
for file in glob.glob(rootdir + "\**\*.png", recursive=True):
    if "retina" in file:
        database_patient_files.append(file)

print("Done")


# for file database_patient_files:
#     if file in combined_diabetic_list:

# file_loc = r"C:\Users\PhilippsLabLaptop\Downloads\DR Stages Matten.xlsx"
# df = pd.read_excel(file_loc, index_col=None, na_values=['NA'], usecols="A,E,F")
# print(df)



# # rootdir = 'path/to/dir'
# for path in glob.glob(f'{rootdir}/*/'):
#     print(path)
# %%
