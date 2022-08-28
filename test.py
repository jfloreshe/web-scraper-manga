import multiprocessing as mp
import cv2
import glob
import os
# file_count_color = sum(len(files) for _, _, files in os.walk(r'images/COLOR'))
# file_count_bw = sum(len(files) for _, _, files in os.walk(r'images/BW'))
# print(file_count_color, file_count_bw)
DESIRED_WIDTH_VALUE = 263

def main(input_folder, output_folder):
    num_cores = mp.cpu_count()
    num_chapters = int(input('num chapters?'))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    processes = []
    for offset in range(num_cores):
        p = mp.Process(target=resize_chapters,args=(input_folder,output_folder,offset*num_chapters + 1,(offset+1)*num_chapters))
        p.start()
        processes.append(p)                                                        
    for p in processes:
        p.join()

def resize_chapters(input_folder, output_folder, start,end):
    for chapter_num in range(start, end+1):
        print(f'Resizing chapter {chapter_num}')
        resize_images(input_folder,output_folder, str(chapter_num))

def resize_images(input_folder, output_folder, chapter):
    chapter = chapter.zfill(3)
    images = [cv2.imread(file) for file in glob.glob(f'{input_folder}\\chapter-{chapter}\\*.jpg')]
    for i in range(len(images)):
        src = images[i]
        height, width, _ = src.shape
        scale_percent = DESIRED_WIDTH_VALUE*100/width
        new_width = int(width * scale_percent/100)
        new_height = int(height * scale_percent/100)
        new_shape = (new_width, new_height)
        output = cv2.resize(src, new_shape)
        cv2.imwrite(f'{output_folder}/{chapter}-{i}.jpg',output) 

if __name__ == '__main__':
    save_folder_bw = 'dataset/BW'
    input_folder_bw = 'images/BW'
    save_folder_color = 'dataset/COLOR'
    input_folder_color = 'images/COLOR'
    main(input_folder_color, save_folder_color)