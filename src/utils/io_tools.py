from pathlib import Path

import tifffile as tf
import numpy as np
from PIL import Image


def image_to_uri(image_array: np.ndarray, tmp_dir: str, image_name: str) -> str:
    """
        Converts a numpy array representing an image into a PNG file, put in a temporary directory and return the URI.
         The image is rotated if its height is greater than its width to ensure correct orientation.

    :param image_array: the numpy array representing an image.
    :param tmp_dir: the temporary directory where the image will be saved.
    :param image_name:  the name of the image to be saved.
    :return:  the URI of the saved image.
    """
    img = Image.fromarray(image_array).convert("RGB")
    if img.height > img.width:
        img = img.rotate(90, expand=True)
    path = Path(tmp_dir) / f"{image_name}.png"
    img.save(path, format="PNG")
    return path.as_uri()

def read_tiff_fast(path, *, series: int = None, level: int = None) -> np.ndarray[tuple[int, int, int]]:
    """
    Fast reading of large tiff image using tifffile with turbojpeg. No metadata included, for that use
    `load_tiff_dataset`. Transposes images to be (Bands, H,W) from (H,W, Bands) since code base already uses that
     format. Also slices away any extra bands outside RGB, since some image manipulation software adds alpha channel band.

    :param level: The level of the image, higher number is lower resolution, 0 is full size.
    :param series: Related images in the same file, only use this if you know what you are doing
    :param path: path to the tiff image.
    :return: the image as array in shape(bands, H, W).
    """

    if series is not None:
        if level is not None:
            img = tf.imread(path, series=series, level=level)
        else:
            img = tf.imread(path, series=series)
    elif level is not None:
        img = tf.imread(path,  level=level)
    else:
        img = tf.imread(path )

    return img[:, :, :3]