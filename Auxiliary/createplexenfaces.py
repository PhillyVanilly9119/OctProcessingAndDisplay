"""
        Script to calcualte the en face images of all segmented OCT data files in a directory 

                            @author: P. Matten
                            @copyright: P. Matten; CMPBME @Medical University of Vienna
                            @contact: philipp.matten@meduniwien.ac.at
"""
import os
import glob
import json 
import matplotlib
import numpy as np
from numba import njit
from tqdm import tqdm
import matplotlib.pyplot as plt

#----------------------------------------------------------------------
# functions
def load_binary(file_path: str, a: int, b: int, c: int) -> np.array:
    """ @param: OCT dimensions: A-scan length, B-scan length and C-scan length 
        @return: numpy-array containing the loaded OCT volume from binary """
    assert os.path.isfile(file_path)
    data = np.reshape(np.fromfile(file_path, dtype='<u1'), (c, b, a))
    data = np.swapaxes(data, 1, -1)
    return data

# abstacter method to generate en face maps 
@njit # check how to use numba for this script
def calculte_enface(data: np.array, key: str="mean") -> None:
    """ @param: np-array containing OCT volume
        @param: key to determine in which way the en face is calculated """
    # calculate en face on the basis of the argmax of every A-scan
    if key.lower() == "argmax" :
        return np.array(np.argmax(data, axis=1), dtype=np.uint8)
    elif key.lower() == "mean" :
        return np.array(np.mean(data, axis=1), dtype=np.uint8)
    elif key.lower() == "median" :
        return np.array(np.median(data, axis=1), dtype=np.uint8)
    elif key.lower() == "upper plexus" :
        print("[WARNING:] Not yet implented")
        return 
    else:
        raise ValueError("Key not implemented... [HINT:] Checke spelling!")

def save_enface_maps(en_face: np.array, file_path: str, image_name: str) -> None: 
    """ save image of en face in two different color maps 
        @param: np.array containing the en face projection of the volume
        @param: path and file name to where the image should be saved """
    matplotlib.image.imsave(os.path.join(os.path.dirname(file_path), image_name.split('.png')[0] + "_jet.png"), en_face, cmap="jet")
    matplotlib.image.imsave(os.path.join(os.path.dirname(file_path), image_name), en_face, cmap="gray")

# crawl through two sub levels of the passed-in main directory
def return_full_list_of_all_files(base: str) -> list:
    """ @param: string containing the main directory 
        @return: list containing all 2nd level (!!!) sub dir folders"""
    dir_list = []
    for name in os.listdir(base):
        if os.path.isdir(os.path.join(base, name)):
            for file in os.listdir(os.path.join(base, name)):
                dir_list.append(os.path.join(base, name, file))
    return dir_list

# run enface image creation on all sub files
def process_data_in_subdirs(a_len: int, b_len: int, path: str) -> None:
    """ file to process all files in a superordinate directory 
        @param: a_len and b_len are the B-scan dimensions """
    onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and "fl_" in f]
    for file in tqdm(onlyfiles):
        file_path = os.path.join(path, file)
        img_name = "ArgmaxEnface_" + file.split(".bin")[0] + ".png"
        # load and process volume data
        data = load_binary(file_path, a_len, b_len, os.path.getsize(file_path)//(a_len*b_len))
        enface = calculte_enface(data)
        # save enface
        save_enface_maps(enface, file_path, img_name)

# crawl through all sub dirs recursively and create en faces for all "flow files"
def process_data_on_server(a_len: int, b_len: int, path: str) -> None:
    """ TODO: implement """
    # ask user to select *.JSON containing sub-paths to the files
    json_file_list = [] 
    valid_data_list = [f for f in glob.glob((path + '/**/*.bin'), recursive = True) if "fl_" in f]
    for file_path in tqdm(valid_data_list):
        print(f"Processing file < {os.path.basename(file_path)} > \nin \n < {os.path.dirname(file_path)} >")
        file = os.path.basename(file_path)
        # skip all files, with wrong dimensions
        if not "1536x2048x" in file:
            print(f"File {file} appears to not have the right dimensions")
            continue 
        # append file path to list
        json_file_list.append(file_path)
        img_name = "ArgmaxEnface_" + file.split(".bin")[0] + ".png"
        # check if this volume was already processed
        c_pic_file_name = os.path.join(os.path.dirname(file_path), img_name.split('.png')[0] + "_jet.png")
        bw_pic_file_name = os.path.join(os.path.dirname(file_path), img_name)
        if os.path.isfile(c_pic_file_name) and os.path.isfile(bw_pic_file_name):
            print(f"Image files \n < {c_pic_file_name} > and \n < {bw_pic_file_name} > already exist!")
            continue
        # load and process volume data
        data = load_binary(file_path, a_len, b_len, os.path.getsize(file_path)//(a_len*b_len))
        enface = calculte_enface(data)
        # save enface
        save_enface_maps(enface, r"C:\Users\PhilippsLabLaptop\Documents\Data\Enfaces", img_name)
    # dump list to file 
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(os.path.join(path,'FileListFlattenedFiles.json'), ensure_ascii=False, indent=4)
    print("[INFO:] Done creating and saving all en face images")
    
#----------------------------------------------------------------------
# main()
def run():
    a_len = 1536
    b_len = 2048
    main_path = r"\\samba\p_Zeiss\Projects\UWF OCTA\Clinical data\MOON1"
    process_data_on_server(a_len, b_len, main_path)
    
#----------------------------------------------------------------------
# "self"-scipt-call to start executing
if __name__ == "__main__":
    run()
    