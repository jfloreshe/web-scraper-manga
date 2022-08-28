from ast import arg
import os
import json
import asyncio
import cv2
import multiprocessing as mp
from urllib import response
import requests
from bs4 import BeautifulSoup

URL_BW = 'https://ww9.readonepiece.com/chapter/one-piece-chapter-'
URL_COLOR = 'https://ww9.readonepiece.com/chapter/one-piece-digital-colored-comics-chapter-'

usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

SAVE_FOLDER = 'images'
BW_FOLDER = 'BW'
COLOR_FOLDER = 'COLOR'

def main():
    num_cores = mp.cpu_count()
    num_chapters = int(input('num chapters?'))
    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)
    if not os.path.exists(f'{SAVE_FOLDER}/{BW_FOLDER}'):
        os.mkdir(f'{SAVE_FOLDER}/{BW_FOLDER}')
    #if not os.path.exists(f'{SAVE_FOLDER}/{COLOR_FOLDER}'):
    #    os.mkdir(f'{SAVE_FOLDER}/{COLOR_FOLDER}')
    processes = []
    for offset in range(num_cores):
        p = mp.Process(target=download_chapters,args=(offset*num_chapters + 1,(offset+1)*num_chapters))
        p.start()
        processes.append(p)                                                        
    for p in processes:
        p.join()

def scrap_onepiece_images(url,chapter):
    search_url = f'{url}{chapter}/'
    response = requests.get(search_url, headers=usr_agent)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    results = soup.select("div[class='my-3'] > div[class='js-pages-container'] > div[class='text-center'] > img")
    url_images = []

    for tag in results:
        url_images.append(tag['src'])
    return url_images

def save_images(folder, images):
    for i, image_url in enumerate(images):
        response = requests.get(image_url)
        image_name = f'{folder}/{i+1}.jpg'
        with open(image_name, 'wb') as file:
            file.write(response.content)


def download_chapters(start, end):
    for chapter_num in range(start, end + 1):
        print(f'Downloading chapter {chapter_num}')
        download_images(str(chapter_num))

def download_images(chapter):
    chapter = chapter.zfill(3)    
    folder_bw = f'{SAVE_FOLDER}/{BW_FOLDER}/chapter-{chapter}'
    #folder_color= f'{SAVE_FOLDER}/{COLOR_FOLDER}/chapter-{chapter}'
    if not os.path.exists(folder_bw):
            os.mkdir(folder_bw)    
    #if not os.path.exists(folder_color):
    #        os.mkdir(folder_color)
    #start_offset = input('Start Offset?')
    #end_offset = input('End Offset?')
    bw_url_images = scrap_onepiece_images(URL_BW, chapter)
    save_images(folder_bw, bw_url_images)

    #color_url_images = scrap_onepiece_images(URL_COLOR, chapter)
    #save_images(folder_color, color_url_images)

if __name__ == '__main__':
    main()