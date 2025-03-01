import os
import glob
import natsort


def delete_file_after_missing_key(file_path_list, key: str="filtered") -> None:
    for folder in file_path_list:
        files = glob.glob(f"{folder}/*.bin")
        files = natsort.natsorted(files)
        for file in files:
            if key not in file:
                os.remove(file)
                print(f"[INFO:] deleted {file}")
            else:
                middle_string = os.path.basename(file).split("rasterVol")[1][:-5]
                os.rename(file, os.path.join(os.path.dirname(file), f"OctVolume_{middle_string}.bin"))


if __name__ == "__main__":

    all_file_paths = [
        r"E:\VolumeRegistration\Eye2_M2_RawVols",
        r"E:\VolumeRegistration\Eye2_M3_RawVols",
        r"E:\VolumeRegistration\Eye2_M4_RawVols",
        r"E:\VolumeRegistration\Eye2_M5_RawVols"
    ]
    delete_file_after_missing_key(all_file_paths)