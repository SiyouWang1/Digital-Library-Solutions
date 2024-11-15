# the 'original' folder has the most complete files
# the 'to_be_checked' folder is a subset of the complete files in terms of filenames

import os
import shutil

original = 'D:\\.....Special_media_images\\Images on PC about Dragomans\\upright-corrected'
to_be_checked = 'C:\\Users\\user\\Desktop\\crop error'
missing_list = 'C:\\Users\\user\\Desktop\\test'

for dirpath, dirnames, filenames_full in os.walk(original):    
    # Sort file names
    filenames_full.sort()

for dirpath1, dirnames1, filenames_to_check in os.walk(to_be_checked):    
    # Sort file names
    filenames_to_check.sort()
print(len(filenames_to_check))
i = 0
j = 0
while i < len(filenames_full):
    if filenames_full[i] == filenames_to_check[j]:
        i += 1
        j += 1
        src_file = os.path.join(original, filenames_full[i])
        dst_file = os.path.join(missing_list, filenames_full[i])
        shutil.copy2(src_file, dst_file)
        print(f'{filenames_full[i]} Copied')
        #print(j)
    else:
        i += 1
    # print(f'i = {i}, j = {j}')