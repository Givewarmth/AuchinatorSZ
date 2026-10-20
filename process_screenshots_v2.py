# Скрипт для обработки скриншотов и поиска их в sandbox/data/items

import os
import glob


def find_matching_icons(screenshots_path, items_path):
    """Найти все файлы с расширениями .png и .jpeg в папке screenshots_path и проверить их наличие в items_path"""
    
    # Проверка существования папок
    if not os.path.exists(screenshots_path):
        print(f"Папка {screenshots_path} не существует")
        return []
    
    if not os.path.exists(items_path):
        print(f"Папка {items_path} не существует")
        return []
    
    # Получение списка скриншотов с расширениями .png и .jpeg
    screenshot_files = []
    
    # Поиск всех .png файлов
    png_files = glob.glob(os.path.join(screenshots_path, "*.png"))
    screenshot_files.extend(png_files)
    
    # Поиск всех .jpeg файлов
    jpeg_files = glob.glob(os.path.join(screenshots_path, "*.jpeg"))
    screenshot_files.extend(jpeg_files)
    
    # Поиск всех .jpg файлов (в случае, если они используют .jpg вместо .jpeg)
    jpg_files = glob.glob(os.path.join(screenshots_path, "*.jpg"))
    screenshot_files.extend(jpg_files)
    
    print(f"Найдено {len(screenshot_files)} файлов скриншотов:")
    for file in screenshot_files:
        print(f"  {os.path.basename(file)}")
        
    # Проверка наличия файлов в папке items
    matching_files = []
    
    for file in screenshot_files:
        filename = os.path.basename(file)
        # Проверяем, есть ли такой файл в папке items
        items_files = glob.glob(os.path.join(items_path, "*"))
        
        for item_file in items_files:
            item_filename = os.path.basename(item_file)
            if item_filename == filename:
                matching_files.append(filename)
                print(f"Найдено совпадение для {filename}")
                
    return matching_files


def main():
    screenshots_path = "sandbox\\data\\screenshots"
    items_path = "sandbox\\data\\items"
    
    matching_files = find_matching_icons(screenshots_path, items_path)
    
    if matching_files:
        print(f"Найдено {len(matching_files)} совпадений:")
        for file in matching_files:
            print(f"  {file}")
    else:
        print("Совпадений не найдено")

if __name__ == "__main__":
    main()