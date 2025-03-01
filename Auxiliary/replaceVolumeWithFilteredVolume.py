
import glob
import numpy as np
from tqdm import tqdm
from scipy import signal


def replace_with_filtered_volume(paths, vol_dims: tuple=(644, 391, 391)) -> None:
    """
    Replace the volume data in the specified files with a filtered version.

    Args:
        paths (List[str]): A list of file paths to the volume files.
        vol_dims (tuple): A tuple specifying the dimensions of the volume data (694, 391, 391).

    Returns:
        None

    Raises:
        None

    Examples:
        replace_with_filtered_volume(["file1.vol", "file2.vol"], (694, 391, 391))
    """
    for file in tqdm(paths):
        vol = np.fromfile(file, dtype=np.uint8).reshape(vol_dims)
        filtered_vol = signal.medfilt(vol, (3,3,3))
        filtered_vol.tofile(file)


if __name__ == "__main__":
    paths = [
        r"E:\VolumeRegistration\20231016_134857_binaries"
    ]
    for path in paths:
        binary_paths = glob.glob(f"{path}/*.bin")
        replace_with_filtered_volume(binary_paths)