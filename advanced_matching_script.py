
import os
import cv2
import numpy as np
from PIL import Image
import json
from pathlib import Path

def find_matches_in_folder():
    """
    Поиск совпадений между скриншотами и иконками в папке data/icons/other
    """
    # Путь к папке с иконками
    icons_path = "data/icons/other"
    
    # Путь к папке с скриншотами
    screenshots_path = "screenshots"
    
    # Проверка существования папок
    if not os.path.exists(icons_path):
        print(f"Папка {icons_path} не существует")
        return None
    
    if not os.path.exists(screenshots_path):
        print(f"Папка {screenshots_path} не существует")
        return None
    
    # Получение списка файлов в папке с иконками
    icon_files = [f for f in os.listdir(icons_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    # Получение списка скриншотов
    screenshot_files = [f for f in os.listdir(screenshots_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    print(f"Найдено {len(icon_files)} иконок в папке {icons_path}")
    print(f"Найдено {len(screenshot_files)} скриншотов в папке {screenshots_path}")
    
    # Создание структуры для хранения информации о сопоставлениях
    matching_data = {
        "total_icons": len(icon_files),
        "total_screenshots": len(screenshot_files),
        "icon_files": icon_files,
        "screenshot_files": screenshot_files,
        "matches": []
    }
    
    # Создание файла для отчета
    with open("matching_report.json", "w") as f:
        json.dump(matching_data, f, indent=2)
    
    print("Отчет о сопоставлениях сохранен в matching_report.json")
    
    return matching_data

# Основная функция
def main():
    print("Поиск совпадений между скриншотами и иконками...")
    
    # Поиск совпадений
    matches = find_matches_in_folder()
    
    if matches:
        print(f"Поиск совпадений завершен успешно")
        print(f"Всего иконок: {matches['total_icons']}")
        print(f"Всего скриншотов: {matches['total_screenshots']}")
    else:
        print("Не удалось найти совпадения")

if __name__ == "__main__":
    main()
