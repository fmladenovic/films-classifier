import requests
import numpy as np
import pandas as pd
import multiprocessing

from bs4 import BeautifulSoup

INPUT_DF = '../for_scraper.csv'
OUTPUT_DF = '../scraped_data.csv'

URL_BASE = 'https://www.imdb.com/title/'

THREADS = 7

def get_poster_url( soup ):
    url = ''
    try:
        url = soup.find('div', {'class':'poster'}).find('img')['src']
    except:
        print('\tCant find poster!')
    return url


def get_summary_text( soup ):
    description = ''
    try:
        description = soup.find('div', {'class':'summary_text'}).decode_contents().strip()
    except:
        print('\tCant find description!')
    return description


def scrape( index, df, return_dict ):
    img_urls = [''] * len(df)
    descriptions = [''] * len(df)
    i = 0
    try:
        for _, row in df.iterrows():
            tconst = row['tconst']
            page = requests.get(URL_BASE + tconst)
            soup = BeautifulSoup( page.content, 'html.parser' )
            img_urls[i] = get_poster_url( soup )
            descriptions[i] = get_summary_text( soup )
            i+=1
    finally:
        return_dict[f'img_url{index}'] = img_urls
        return_dict[f'description{index}'] = descriptions

if __name__ == "__main__":
    df = pd.read_csv(INPUT_DF)
    dfs = np.array_split(df, THREADS)
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    jobs = []
    for i, df in enumerate(dfs):
        p = multiprocessing.Process(target=scrape, args=(i, df, return_dict))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    for i, df in enumerate(dfs):
        df['img_url'] = return_dict.get(f'img_url{i}')
        df['description'] = return_dict.get(f'description{i}')

    labels = np.arange(1, 10.1, 0.1)


    new_df = pd.concat(dfs)
    new_df.to_csv(OUTPUT_DF, index = False)
    print("Saved csv...")


