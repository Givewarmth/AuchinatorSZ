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


def load_mapping_data(mapping_file):
    """Загружает данные сопоставления"""
    try:
        with open(mapping_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл сопоставления {mapping_file} не найден.")
        return None
    except json.JSONDecodeError:
        print(f"Ошибка чтения JSON файла {mapping_file}.")
        return None


def find_matches_in_folders(icon_folders):
    """Находит совпадения в указанных папках"""
    matches = []
    
    for folder in icon_folders:
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        full_path = os.path.join(root, file)
                        matches.append(full_path)
    return matches


def find_matches_recursive():
    """Находит совпадения в рекурсивных подпапках"""
    
    # Путь к папке с иконками
    icons_folder = "data/icons"
    
    # Путь к файлу сопоставления
    mapping_file = "mapping_report.json"
    
    # Получаем список всех файлов иконок
    all_icon_files = find_all_icon_files(icons_folder)
    
    # Читаем файл сопоставления
    mapping_data = load_mapping_data(mapping_file)
    
    if mapping_data is None:
        return
    
    print(f"Найдено {len(all_icon_files)} файлов иконок в подпапках {icons_folder}")
    print(f"Данные сопоставления: {mapping_data}")
    
    # Проверяем, есть ли в данных сопоставления информация о идентификаторах
    if "mapping_details" in mapping_data:
        details = mapping_data["mapping_details"]
        print(f"Детали сопоставления:")
        print(f"  - Всего совпадений: {details.get('total_matches', 0)}")
        print(f"  - Дублирующиеся ID: {details.get('duplicate_ids', [])}")
        print(f"  - Действительные элементы: {details.get('valid_items', [])}")
    
    return all_icon_files

if __name__ == "__main__":
    find_matches_recursive()