import os
import cv2
import numpy as np
import concurrent.futures

THREADS = 7

IMAGES_PATH = '../data_imgs_test/'
OUTPUT_IMAGES_PATH = '../data_imgs_test_resized/'

def resize( image_names ):
    for image_name in image_names:
        image = cv2.imread(IMAGES_PATH + image_name, cv2.IMREAD_UNCHANGED)
        output = cv2.resize( image, (224, 224))
        cv2.imwrite(OUTPUT_IMAGES_PATH + image_name, output) 

if __name__ == "__main__":
    image_names = os.listdir(IMAGES_PATH)
    lists = np.array_split( image_names, THREADS)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(resize, lists)
    print("Resized images...")