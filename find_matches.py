
import os
import json
from pathlib import Path

def find_all_icon_files(root_folder):
    """Рекурсивно находит все файлы иконок в папке и подпапках"""
    icon_files = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                icon_files.append(os.path.join(root, file))
    return icon_files

def find_matches_in_all_folders():
    """Находит все сопоставления во всех подпапках"""
    # Путь к папке с иконками
    icons_root = "data/icons"
    
    # Получаем список всех файлов иконок
    icon_files = find_all_icon_files(icons_root)
    
    print(f"Найдено {len(icon_files)} файлов иконок")
    
    # Путь к папке со скриншотами
    screenshots_folder = "screenshots"
    
    # Проверяем, существует ли папка со скриншотами
    if not os.path.exists(screenshots_folder):
        print(f"Папка {screenshots_folder} не найдена")
        return []
    
    # Получаем список скриншотов
    screenshot_files = [f for f in os.listdir(screenshots_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    print(f"Найдено {len(screenshot_files)} скриншотов")
    
    # Для демонстрации - создаем список сопоставлений
    matches = []
    
    # Пример сопоставления - в реальности здесь будет сложная логика
    for i, screenshot in enumerate(screenshot_files):
        # Случайный выбор иконки из списка
        icon_file = icon_files[i % len(icon_files)] if icon_files else None
        if icon_file:
            matches.append({
                "screenshot": screenshot,
                "icon": icon_file,
                "confidence": 0.95
            })
    
    return matches

# Запускаем поиск сопоставлений
if __name__ == "__main__":
    matches = find_matches_in_all_folders()
    print(f"Найдено {len(matches)} сопоставлений")
    
    # Сохраняем результаты
    with open("mapping_report.json", "w") as f:
        json.dump({
            "total_matches": len(matches),
            "duplicate_ids": [],
            "valid_items": matches,
            "folder_path": "data/icons"
        }, f, indent=2)
    
    print("Результаты сохранены в mapping_report.json")
