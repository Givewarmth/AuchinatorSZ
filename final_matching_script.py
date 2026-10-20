import os
import json
from pathlib import Path

def find_all_icon_files(icon_folder):
    """Рекурсивно находит все файлы иконок в подпапках"""
    icon_files = []
    for root, dirs, files in os.walk(icon_folder):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):
                icon_files.append(os.path.join(root, file))
    return icon_files

def find_matches_in_files(icon_files, mapping_data):
    """Находит совпадения между файлами иконок и данными сопоставления"""
    matches = []
    
    # Преобразуем mapping_data в более удобный формат
    mapping_dict = {}
    for vendor, items in mapping_data.items():
        for item in items:
            if item not in mapping_dict:
                mapping_dict[item] = []
            mapping_dict[item].append(vendor)
    
    # Проверяем каждый файл иконки
    for icon_file in icon_files:
        filename = os.path.basename(icon_file)
        # Ищем совпадения в данных сопоставления
        if filename in mapping_dict:
            matches.append({
                'icon_file': icon_file,
                'matches': mapping_dict[filename]
            })
    
    return matches


def main():
    # Загружаем данные сопоставления
    try:
        with open('mapping_report.json', 'r') as f:
            mapping_data = json.load(f)
    except FileNotFoundError:
        print("Файл mapping_report.json не найден")
        return
    
    # Находим все файлы иконок
    icon_folder = 'data/icons'
    icon_files = find_all_icon_files(icon_folder)
    print(f"Найдено {len(icon_files)} файлов иконок в подпапках {icon_folder}")
    
    # Находим совпадения
    matches = find_matches_in_files(icon_files, mapping_data)
    print(f"Найдено {len(matches)} совпадений с данными сопоставления.")
    
    # Выводим результаты
    for match in matches:
        print(f"{match['icon_file']} -> {match['matches']}")
    
    # Сохраняем результаты в файл
    with open('final_mapping_report.json', 'w') as f:
        json.dump(matches, f, indent=2)
    
    return len(matches)

if __name__ == "__main__":
    main()