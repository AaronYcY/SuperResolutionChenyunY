import cv2
import numpy as np


def read_image(image_file):
    image = cv2.imread(image_file)
    return image


def normalize_image(image):
    image = (image / 127.5 - 1).astype(np.float32)
    return image


def normalized_array_to_image(array):
    image = ((array + 1.0) * 127.5).astype(np.uint8)
    return image


def concat_two_images_horizontal(image1, image2):
    h1, w1, c1 = image1.shape
    h2, w2, c2 = image2.shape
    if c1 != c2:
        print("channels not match.")
        return

    if h1 > h2:
        tmp = np.zeros([h1-h2, w2, c1])
        image3 = np.vstack([image2, tmp])
        image3 = np.hstack([image1, image3])
    elif h1 == h2:
        image3 = np.hstack([image1, image2])
    else:
        tmp = np.zeros([h2-h1, w1, c2])
        image3 = np.vstack([image1, tmp])
        image3 = np.hstack([image3, image2])
    return image3


def concat_two_images_vertical(image1, image2):
    h1, w1, c1 = image1.shape
    h2, w2, c2 = image2.shape
    if c1 != c2:
        print("channels not match.")
        return

    if w1 > w2:
        tmp = np.zeros([h2, w1-w2, c1])
        image3 = np.hstack([image2, tmp])
        image3 = np.vstack([image1, image3])
    elif w1 == w2:
        image3 = np.vstack([image1, image2])
    else:
        tmp = np.zeros([h1, w2-w1, c2])
        image3 = np.hstack([image1, tmp])
        image3 = np.vstack([image3, image2])
    return image3


def concat_images_horizontal(images):
    if len(images) <= 0:
        return
    image = images[0]
    for i in range(1, len(images)):
        image = concat_two_images_horizontal(image, images[i])
    return image


def concat_images_vertical(images):
    if len(images) <= 0:
        return
    image = images[0]
    for i in range(1, len(images)):
        image = concat_two_images_vertical(image, images[i])
    return image
