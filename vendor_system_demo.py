"""
Демонстрация работы с системой обработки скриншотов вендора
"""

import os
import json

def main():
    print("=== СИСТЕМА ОБРАБОТКИ СКРИНШОТОВ ВЕНДОРА ===")
    
    # Проверяем наличие ключевых файлов
    files_to_check = [
        'vendor_data.txt',
        'items_data.txt', 
        'mapping.json',
        'screenshots/',
        'icons/'
    ]
    
    print("Наличие необходимых файлов:")
    for file in files_to_check:
        if file.endswith('/'):
            exists = os.path.isdir(file[:-1])
        else:
            exists = os.path.exists(file)
        status = "✓" if exists else "✗"
        print(f"  {status} {file}")
    
    # Анализ данных вендора
    print("
=== АНАЛИЗ ДАННЫХ ВЕНДОРА ===")
    
    # Показываем содержимое vendor_data.txt
    try:
        with open('vendor_data.txt', 'r') as f:
            lines = f.readlines()
            print("Предметы в вендоре:")
            for i, line in enumerate(lines):
                line = line.strip()
                if line and not line.startswith('#'):
                    print(f"  {i+1}. {line}")
    except FileNotFoundError:
        print("vendor_data.txt: не найден")
    
    # Показываем содержимое items_data.txt
    try:
        with open('items_data.txt', 'r') as f:
            lines = f.readlines()
            print("Данные предметов:")
            for i, line in enumerate(lines):
                line = line.strip()
                if line and not line.startswith('#'):
                    print(f"  {i+1}. {line}")
    except FileNotFoundError:
        print("items_data.txt: не найден")
    
    # Показываем содержимое mapping.json
    try:
        with open('mapping.json', 'r') as f:
            mapping = json.load(f)
            print("Сопоставление иконок:")
            for key, value in list(mapping.items())[:5]:  # Показываем первые 5
                print(f"  {key}: {value}")
            if len(mapping) > 5:
                print("  ... и еще {} записей".format(len(mapping) - 5))
    except (FileNotFoundError, json.JSONDecodeError):
        print("mapping.json: не найден или поврежден")
    
    # Показываем доступные скрипты
    print("
=== ДОСТУПНЫЕ СКРИПТЫ ===")
    scripts = [
        'check_vendor_screenshot.py',
        'screenshot_processor.py', 
        'vendor_screenshot_processor.py',
        'screenshot_analyzer.py',
        'compare_images.py',
        'icon_price_matcher.py'
    ]
    
    for script in scripts:
        exists = os.path.exists(script)
        status = "✓" if exists else "✗"
        print(f"  {status} {script}")
    
    print("
=== РЕКОМЕНДАЦИИ ===")
    print("Для работы с системой:")
    print("1. Убедитесь, что все файлы vendor_data.txt, items_data.txt, mapping.json существуют")
    print("2. Проверьте наличие скриншотов в папке screenshots/")
    print("3. Проверьте наличие иконок в папке icons/")
    print("4. Запустите vendor_screenshot_processor.py для обработки данных")

if __name__ == "__main__":
    main()
