import os
import json
from pathlib import Path

def find_all_icon_files(root_folder):
    """Рекурсивно находит все файлы иконок в подпапках"""
    icon_files = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                icon_files.append(os.path.join(root, file))
    return icon_files

def find_matches_recursive():
    """Находит совпадения в рекурсивных подпапках"""
    # Путь к папке с иконками
    icons_folder = "data/icons"
    
    # Получаем список всех файлов иконок
    all_icon_files = find_all_icon_files(icons_folder)
    
    # Путь к файлу сопоставления
    mapping_file = "mapping_report.json"
    
    # Проверяем, существует ли файл сопоставления
    if not os.path.exists(mapping_file):
        print(f"Файл сопоставления {mapping_file} не найден.")
        return
    
    # Читаем файл сопоставления
    with open(mapping_file, 'r') as f:
        mapping_data = json.load(f)
    
    print(f"Найдено {len(all_icon_files)} файлов иконок в подпапках {icons_folder}")
    print(f"Данные сопоставления: {mapping_data}")
    
    # Здесь можно добавить логику для поиска совпадений
    # Например, сравнение с данными из mapping_data
    
    return all_icon_files

if __name__ == "__main__":
    find_matches_recursive()