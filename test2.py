from email.mime import image
from genericpath import isfile
import os
import glob
import shutil

file_count_color = sum(len(files) for _, _, files in os.walk(r'dataset/COLOR'))
file_count_bw = sum(len(files) for _, _, files in os.walk(r'dataset/BW'))
color_test_total = int(file_count_color*30/100)
bw_test_total = int(file_count_bw*30/100)
images_color = [path for path in glob.glob('dataset\\COLOR\\*.jpg')]
images_bw = [path for path in glob.glob('dataset\\BW\\*.jpg')]

test_bw_destination_folder = 'dataset/TEST_BW/'
test_color_destination_folder = 'dataset/TEST_COLOR/'
# for i in range(color_test_total):
#     input_path = images_color[i]
#     name = images_color[i].split('\\')[-1]
#     output_path = test_color_destination_folder + name
#     if os.path.isfile(input_path):
#         shutil.move(input_path, output_path)        
#         print(f'moved from {input_path} to {output_path}')

for i in range(bw_test_total):
    input_path = images_bw[i]
    name = images_bw[i].split('\\')[-1]
    output_path = test_bw_destination_folder + name
    if os.path.isfile(input_path):
        shutil.move(input_path, output_path)        
        print(f'moved from {input_path} to {output_path}')
