import os
from typing import *
from PIL import Image, ImageFilter, ImageOps
import skimage
from skimage import filters
import numpy as np
import glob
import sys

PREVIEW_SIZE = (640, 480)


#function definitions
def open_image(image: str,
               size: Optional[Tuple[int, int]] = None) -> Image.Image:
    path = os.path.join(image)
    im = Image.open(path)
    if size is not None:
        im.thumbnail(size, Image.ANTIALIAS)
    return im


def normalize(arr: np.ndarray) -> np.ndarray:
    min_, max_ = arr.min(), arr.max()
    return (arr - min_) / (max_ - min_)


def to_array(im: Image.Image) -> np.ndarray:
    return np.array(im, dtype=np.float32) / 255.


def to_image(arr: np.ndarray, normalize_image: bool = True) -> Image.Image:
    arr = normalize(arr) if normalize_image else arr
    return Image.fromarray((arr * 255.).astype(np.uint8))


def open_dataset(
        name: str,
        size: Optional[Tuple[int, int]] = PREVIEW_SIZE) -> List[Image.Image]:
    return [open_image(pth, size) for pth in image_sets[name]]


def grayscale_intensity(im: Image.Image) -> Image.Image:
    g = to_array(im).mean(axis=2)
    return to_image(g)


def grayscale_gleam(im: Image.Image) -> Image.Image:
    g = np.power(to_array(im), 1 / 2.2).mean(axis=2)
    return to_image(g)


def laplace(arr: np.ndarray,
            kernel_size=3,
            square: bool = False) -> np.ndarray:
    gradients = filters.laplace(arr, kernel_size)
    return gradients * gradients if square else gradients


interp = str(sys.argv[1])
folder = str(sys.argv[2])

im_objs = []
tomo_pics = glob.glob("images/{}/{}/*png".format(folder, interp))
image_sets = {'test_1': tomo_pics}

imgs_test_1 = open_dataset('test_1')
# print(imgs_test_1)

im_objs.append(grayscale_intensity(imgs_test_1[-1]))
im_objs.append(grayscale_gleam(imgs_test_1[-1]))

im_objs.append(to_image(laplace(to_array(grayscale_gleam(imgs_test_1[0])), 3)))
im_objs.append(to_image(laplace(to_array(grayscale_gleam(imgs_test_1[-1])),
                                3)))
im_objs.append(
    to_image(
        laplace(to_array(grayscale_gleam(imgs_test_1[-1])), 3, square=True)))
im_objs.append(
    to_image(
        laplace(to_array(grayscale_gleam(imgs_test_1[-1])), 3,
                square=True)**0.5))

arrs_test_1 = [to_array(grayscale_gleam(img)) for img in imgs_test_1]

energies_test_1 = np.stack(
    [laplace(arr, 3, square=True) for arr in arrs_test_1], axis=2)

#energies_test_1.shape

highest_energies_idx = np.argmax(energies_test_1, axis=2)
#highest_energies_idx

source = np.stack(arrs_test_1, axis=0)
#source.shape

fused_array = np.zeros(energies_test_1.shape[0:2], dtype=np.float32)
rows, cols = fused_array.shape
for row in range(rows):
    for col in range(cols):
        idx = highest_energies_idx[row, col]
        fused_array[row, col] = source[idx, row, col]

im_objs.append(to_image(fused_array))

source_color = np.stack(imgs_test_1, axis=0)
#source_color.shape

height, width = energies_test_1.shape[0:2]
fused_array_color = np.zeros((height, width, 3), dtype=np.float32)
rows, cols = fused_array.shape

for row in range(rows):
    for col in range(cols):
        idx = highest_energies_idx[row, col]
        #print(source_color[idx, row, col, :])
        fused_array_color[row, col, :] = source_color[idx, row, col, :][:-3]

im_objs.append(to_image(fused_array_color))

normalized_indexes = normalize(highest_energies_idx)

normalized_indexes_blurred = skimage.filters.gaussian(normalized_indexes, 1.4)
im_objs.append(to_image(normalized_indexes_blurred))

im_objs[0].save("result/{}/{}.pdf".format(folder, interp),
                save_all=True,
                append_images=im_objs)
