import os
import numpy as np
import pandas as pd
import cv2
import concurrent.futures

THREADS = 2

IMAGES_PATH = '../data_imgs_preprocessed/'
OUTPUT_IMAGES_PATH = '../data_imgs_10_per/'

TRAIN_DF = '../train_10_per.csv'
TEST_DF = '../test_10_per.csv'

def cpy( df ):
    image_names = df['tconst']
    for image_name in image_names:
        image = cv2.imread(IMAGES_PATH + image_name + '.jpg', cv2.IMREAD_UNCHANGED)
        output = cv2.resize( image, (224, 224))
        cv2.imwrite(OUTPUT_IMAGES_PATH + image_name + '.jpg', output) 

if __name__ == "__main__":

    train = pd.read_csv(TRAIN_DF)
    test = pd.read_csv(TEST_DF) 
    df = pd.concat([train, test])
    dfs = np.array_split( df, THREADS)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(cpy, dfs)
    print("Finish...")