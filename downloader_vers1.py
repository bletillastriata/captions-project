"""
Note: This script works best with at least 8GB of RAM. A new version that uses less memory and fewer resources
is currently in development. Once the new version is complete, this version will kept as a legacy only and will 
not be supported in future developments.
"""

# Author: Siyuan (Kevin) Peng
# Require python version 3.6+


import requests
from requests import Response
from multiprocessing import Pool, Process, Manager, Queue
from multiprocessing.pool import ThreadPool # Grey's addition
import os
from shutil import copyfile

path = os.path
mkdir = os.mkdir

# Define the directory to tsv file

# instance address
training_file_dir: str = '/home/admin/Train_GCC-training.tsv'
# local address: 
# training_file_dir: str = 'E:/Downloads/Train_GCC-training.tsv'

# Define the directory to file that stores downloaded jpeg file
# instance address
jpeg_folder_path: str = '/home/admin/data/jpeg_file/'
# local address:
# jpeg_folder_path: str = 'C:/Users/Tuge/Desktop/test_folder/'

# Define the directory to file that stores downloaded non-jpeg file
# instance address
none_jpeg_folder_path: str = '/home/admin/data/none_jpeg_file/'
# local address
#none_jpeg_folder_path: str = 'C:/Users/Tuge/Desktop/test_folder2/'

# Define the directory to store the error log file
# instance address:
error_log_path: str = '/home/admin/'
# local address:
#error_log_path: str = 'E:/Study/FIRE 171/Project/Fire/'

# Define the maximum number of image and suggested value is 3500000
max_image_num: int = 2000
# Define the starting position for downloading
start_pos: int = 0
# Define the maximum number of thread.
# I use 1000 threads for downloading(32G internal memory + i5-9600 CPU)
max_concurrent_download: int = 128
STOP_TOKEN: str = '##stop##'


# Define the function that download one image with url
def down_image(txt_str: str, img_url: str, count: int, queue: Queue):
    print(f'count = {count}', end='\t')
    file_dir_suffix: str = f'{count}/'
    img_name: str = 'img.jpg'
    txt_name: str = 'text.txt'

    # Try to determine if file is already created
    if path.isfile(jpeg_folder_path + file_dir_suffix + img_name):
        print(f'         × Imag {count:3} already downloaded')

        # copy_file(count, file_dir_suffix, img_name)
    else:
        try:
            r = requests.get(img_url, stream=True, timeout=10)
            content_types = requests.head(img_url).headers.get('content-type')
            if content_types is None:
                print('content_types is None')
                download_image_with_dir(
                    none_jpeg_folder_path + file_dir_suffix, img_name, r,
                    count)
                write_img_description(none_jpeg_folder_path + file_dir_suffix + txt_name, txt_str, count)

                return
            else:
                content_types = content_types.split('/')

            if r.status_code == 200:
                if 'jpeg' in content_types:  # if the website looks fine
                    print('jpeg in content_types')
                    download_image_with_dir(jpeg_folder_path + file_dir_suffix,
                                            img_name, r, count)
                    write_img_description(jpeg_folder_path + file_dir_suffix + txt_name, txt_str, count)
                else:
                    print('jpeg not in content_types')
                    content: str = f' x img {count:3} This is possibly an image and is not jpeg'
                    queue.put(content)
                    download_image_with_dir(
                        none_jpeg_folder_path + file_dir_suffix, img_name, r,
                        count)
                    write_img_description(none_jpeg_folder_path + file_dir_suffix + txt_name, txt_str, count)
                    return
            else:
                # Error handling Below
                content: str = f' × Imag {count:3} status code error: {r.status_code}'
                queue.put(content)
                return
        except Exception as e:
            content: str = f' × Imag {count:3} downloading raised exception: {e} \n with URL:{img_url}'
            queue.put(content)
            return


def download_image_with_dir(dir_path: str, img: str, r: Response, count: int):
    if not path.isdir(dir_path):
        mkdir(dir_path)
    with open(dir_path + img, 'wb') as file:
        for chunk in r:
            file.write(chunk)
        print(f'         √ Imag {count:3} just downloaded <- {r.url}')


def write_img_description(store_path: str, text: str, count:int):
    # Determine if the txt file is already created in none jpeg folder
    # none_jpeg_folder_path + file_dir_suffix + txt_name
    if path.isfile(store_path):
        print(f'         × Text {count:3} already created')
    else:
        # create txt file here
        with open(store_path, 'w') as file:
            file.write(text)
        print(f'         √ Text {count:3} is created')


def write_file(file_name: str, queue: Queue):
    # print('writing file')
    with open(file_name, 'a', 1) as f:
        while True:
            q_get = queue.get()
            if q_get == STOP_TOKEN:
                break
            else:
                print(f'writing:{q_get}')
                f.write(f'{q_get}\n')
    # print('end writing file')


# Main Method
if __name__ == '__main__':
    queue: Queue = Manager().Queue()
    current_image_num: int = 0
    print(' *** Starting... ***')

    #pool = Pool(max_concurrent_download + 1)
    pool = ThreadPool(max_concurrent_download + 1) # Grey's addition
    pool.apply_async(write_file, (f'{error_log_path}error_log.txt', queue))
    # print('opening')

    with open(training_file_dir, encoding='utf-8') as url:
        for line in url:
            current_image_num += 1
            if current_image_num < start_pos:
                continue
            if current_image_num > max_image_num:
                break
            tab_position = line.find("\t")
            txt_str = line[:tab_position]
            img_url = line[tab_position:]

            pool.apply_async(
                down_image,
                (txt_str.strip(), img_url.strip(), current_image_num, queue))

    print('closing pool')
    pool.close()
    print('joining pool')
    queue.put(STOP_TOKEN)
    pool.join()
    print('All Done!')
