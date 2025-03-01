"""
Script for Continuous Volume Registration project with TUM in Munich 
"""

import os
import glob
import natsort


def run():
    shape = (694,391,391)
    paths = [
        r"D:\VolumeRegistration\Eye2_M1_RawVols",
        r"D:\VolumeRegistration\Eye2_M2_RawVols",
        r"D:\VolumeRegistration\Eye2_M3_RawVols",
        r"D:\VolumeRegistration\Eye2_M4_RawVols",
        r"D:\VolumeRegistration\Eye2_M5_RawVols"
    ]
    for path_main_folder in paths:
        all_vol_files = glob.glob(path_main_folder + "/*.bin")
        all_vol_files = natsort.natsorted(all_vol_files)
        for file in all_vol_files:
            if not "filtered" in file:
                os.remove(file)
                print(f"[INFO:] Deleted {file}")
        final_file_list = glob.glob(path_main_folder + "/*.bin")
        final_file_list = natsort.natsorted(final_file_list)
        for f_file in final_file_list:
            new_file_name = os.path.join(os.path.dirname(f_file), "OctVolume_" + f_file.split("rasterVol")[1][:-5] + ".bin")
            os.rename(f_file, new_file_name)
            print(f"[INFO:] Renaming {new_file_name}")
    

if __name__ == "__main__":
    run()