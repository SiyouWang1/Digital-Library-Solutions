import os
import shutil

src_root = 'C:\\D\\DSU\\Kanagaratnam\\test_rotation\\76_INTERNATIONAL TAMIL\'S ARCHIVES KANDY_ TO'
dst_folder = 'C:\\D\\DSU\\Kanagaratnam\\test_rotation\\76_sample'


def create_sample(src_root, dst_folder, every_nth, mode):
    counter = 1
    
    # Create the destination folder if it doesn't exist
    os.makedirs(dst_folder, exist_ok=True)
    
    # Walk through all directories and files in the source root
    for root, dirs, files in os.walk(src_root):
        for file in files:
            counter += 1
            # Construct full file path
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dst_folder, f'75{file}')
            
            if counter % every_nth == 0:
                # Move every 2 file to the destination folder
                if mode == 'copy':
                    shutil.copy2(src_file, dst_file)
                    print(f"Moved {src_file} to {dst_file}")
                else:
                    shutil.move(src_file, dst_file)
                    print(f"Moved {src_file} to {dst_file}")


create_sample(src_root, dst_folder, 8, 'copy')