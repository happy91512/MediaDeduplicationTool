import os
import shutil
import glob
from typing import List
import cv2
from PIL import Image
import imagehash

def get_filenames(dir_path: str, specific_name: str, withDirPath=True) -> List[str]:
    '''
    This function is editted by YU-SHUN,
    Welcome to contact me if you have any questions.
    e-mail: tw.yshuang@gmail.com
    Github: https://github.com/tw-yshuang
    -----
    get_filenames
    -----
    This function can find any specific name under the dir_path, even the file inside directories.

    specific_name:
        >>> Can type any word or extension.
        e.g. '*cat*', '*.csv', '*cat*.csv',
    '''

    if dir_path[-1] != '/':
        dir_path += '/'

    filenames = glob.glob(f'{dir_path}**/{specific_name}', recursive=True)

    if '*.' == specific_name[:2]:
        filenames.extend(glob.glob(f'{dir_path}**/{specific_name[1:]}', recursive=True))

    if withDirPath is False:
        dir_path_len = len(dir_path)
        filenames = [filename[dir_path_len:] for filename in filenames]

    return filenames

def copy_file(file_path, output_folder):
    """Copy file to the specified output folder."""
    try:
        dest_path = os.path.join(output_folder, os.path.basename(file_path))
        shutil.copy2(file_path, dest_path)
        return file_path  # Return the copied file path
    except Exception as e:
        print(f"Error copying {file_path}: {e}")
        return None

def merge_target_files(disk_list, target_extensions):
    files = []
    for disk in disk_list:
        for extension in target_extensions:
            files += get_filenames(disk, f'*{extension}')
    return files

def get_perceptual_hash(image):
    return imagehash.phash(image)

def extract_fifth_frame(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_count < 5:
        cap.release()
        return None

    cap.set(cv2.CAP_PROP_POS_FRAMES, 4)
    ret, frame = cap.read()
    cap.release()
    
    return frame if ret else None

def convert_frame_to_pil(frame):
    return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

def process_file(file_path, is_video=False):
    if is_video:
        frame = extract_fifth_frame(file_path)
        if frame is not None:
            img = convert_frame_to_pil(frame)
            img_hash = get_perceptual_hash(img)
            return file_path, img_hash
    else:
        try:
            img = Image.open(file_path)
            img_hash = get_perceptual_hash(img)
            return file_path, img_hash
        except:
            return file_path, None
    return None

def are_images_similar(hash1, hash2, threshold=5):
    return hash1 - hash2 < threshold