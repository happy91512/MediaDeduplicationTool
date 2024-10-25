import os
import csv
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from tool import *


def deduplicate_files(file_list, output_folder, is_video=False, include_errors=False, threshold=3):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    unique_files = []
    seen_hashes = {}
    csv_file_path = os.path.join(output_folder, 'similar_files.csv')
    
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['File 1', 'File 2', 'Similarity'])
        writer.writeheader()

        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            future_to_file = {executor.submit(process_file, file_path, is_video): file_path for file_path in file_list}
            for future in tqdm(as_completed(future_to_file), total=len(future_to_file)):
                result = future.result()
                if result:
                    file_path, img_hash = result
                    if img_hash is None and include_errors:
                        unique_files.append(file_path)
                        continue

                    is_unique = True
                    for seen_hash, seen_path in seen_hashes.items():
                        if are_images_similar(img_hash, seen_hash, threshold=threshold):
                            is_unique = False
                            writer.writerow({'File 1': file_path, 'File 2': seen_path, 'Similarity': img_hash - seen_hash})
                            csvfile.flush()
                            break
                    
                    if is_unique:
                        seen_hashes[img_hash] = file_path
                        unique_files.append(file_path)

    return unique_files


if __name__ == "__main__":
    disk_list = input("Enter the disk locations to check (separated by commas): ").split(',')
    disk_list = [disk.strip() for disk in disk_list]

    output_path = input("Enter the output folder path: ")
    
    include_errors = input("Include videos with errors in the copy list? (y/n): ").lower() == 'y'
    if include_errors:
        include_without_encode = input("Enter specific file extensions without hash calculation (separated by commas): ")
        include_without_encode = [extension.strip() for extension in include_without_encode]
    
    image_extensions = ["bmp", "jpg", "jpeg", "png", "gif"]
    video_extensions = ["mp4", "mov"]
    

    images = merge_target_files(disk_list, image_extensions)
    videos = merge_target_files(disk_list, video_extensions)
    print('Number of images needing hash calculation.: ', len(images))
    print('Number of videos needing hash calculation.: ', len(videos))

    save_images = deduplicate_files(images, output_path)
    unique_videos = deduplicate_files(videos, output_path, is_video=True, include_errors=include_errors)
    
    if include_errors:
        unique_videos += merge_target_files(disk_list, include_without_encode)
    print('Saving unique images and videos to destination...')
    
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(copy_file, file_path, output_path) for file_path in (save_images + unique_videos)]
        
        for future in tqdm(as_completed(futures), total=len(futures)):
            result = future.result()
            if not result:
                print(f"Failed to copy {result}.")
    print('=' * 20, 'Mission accomplished!', '=' * 20)
    print('Unique images number: ', len(save_images))
    print('Unique videos number: ', len(unique_videos))