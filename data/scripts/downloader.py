import requests
import numpy as np
import pandas as pd
import concurrent.futures

INPUT_DF = '../data.csv'
OUTPUT_FOLDER = '../data_imgs/'

THREADS = 7

def download( df ):
    for _, row in df.iterrows():
        tconst = row['tconst']
        name = OUTPUT_FOLDER + f'/{tconst}.jpg'
        with open(name, 'wb') as handle:
            url = row['img_url']
            response = requests.get(url, stream=True)
            if not response.ok:
                print(response)
            for block in response.iter_content(182):
                if not block:
                    break
                handle.write(block)


if __name__ == "__main__":
    df = pd.read_csv(INPUT_DF)
    dfs = np.array_split(df, THREADS)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(download, dfs)
    print("Saved images...")


