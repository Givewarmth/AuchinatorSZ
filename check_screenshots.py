# Скрипт для проверки всех файлов с расширениями .png и .jpeg в папке sandbox/data/screenshots

import os
import glob

def check_screenshots(screenshots_path):
    """Проверить все файлы с расширениями .png и .jpeg в указанной папке"""
    
    # Проверка существования папки
    if not os.path.exists(screenshots_path):
        print(f"Папка {screenshots_path} не существует")
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
    
    # Вывод информации о каждом файле
    for file in screenshot_files:
        filename = os.path.basename(file)
        file_size = os.path.getsize(file)
        print(f"  {filename} (размер: {file_size} байт)")
        
    return screenshot_files


def main():
    screenshots_path = "sandbox\data\screenshots"
    
    screenshot_files = check_screenshots(screenshots_path)
    
    if screenshot_files:
        print(f"Всего найдено {len(screenshot_files)} файлов скриншотов.")
    else:
        print("В папке не найдено файлов с расширениями .png или .jpeg.")

if __name__ == "__main__":
    main()