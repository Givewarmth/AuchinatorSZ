
"""
Система обработки скриншотов вендора для Stalfarm
"""

import os
import json
from pathlib import Path

def check_files():
    """Проверка наличия необходимых файлов"""
    required_files = [
        'vendor_data.txt',
        'items_data.txt',
        'mapping.json',
        'screenshots/',
        'icons/'
    ]
    
    print("=== ПРОВЕРКА КОМПЛЕКТНОСТИ ===")
    for file in required_files:
        if file.endswith('/'):
            exists = os.path.isdir(file[:-1])
        else:
            exists = os.path.exists(file)
        status = "✓" if exists else "✗"
        print(f"  {status} {file}")
    
    return all(os.path.exists(f[:-1]) if f.endswith('/') else os.path.exists(f) for f in required_files)

def analyze_vendor_data():
    """Анализ данных вендора"""
    print("
=== АНАЛИЗ ДАННЫХ ВЕНДОРА ===")
    
    try:
        with open('vendor_data.txt', 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
            print(f"Найдено {len(lines)} предметов в вендоре:")
            for i, line in enumerate(lines, 1):
                print(f"  {i}. {line}")
    except FileNotFoundError:
        print("vendor_data.txt: файл не найден")
        return []

def analyze_items_data():
    """Анализ данных предметов"""
    print("
=== АНАЛИЗ ДАННЫХ ПРЕДМЕТОВ ===")
    
    try:
        with open('items_data.txt', 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
            print(f"Найдено {len(lines)} предметов:")
            for i, line in enumerate(lines, 1):
                print(f"  {i}. {line}")
    except FileNotFoundError:
        print("items_data.txt: файл не найден")
        return []

def analyze_mapping():
    """Анализ сопоставления иконок"""
    print("
=== АНАЛИЗ СОПОСТАВЛЕНИЯ ИКОНОК ===")
    
    try:
        with open('mapping.json', 'r') as f:
            mapping = json.load(f)
            print(f"Найдено {len(mapping)} записей в mapping.json:")
            for i, (key, value) in enumerate(list(mapping.items())[:5]):  # Показываем первые 5
                print(f"  {i+1}. {key}: {value}")
            if len(mapping) > 5:
                print(f"  ... и еще {len(mapping) - 5} записей")
    except (FileNotFoundError, json.JSONDecodeError):
        print("mapping.json: файл не найден или поврежден")
        return {}

def process_screenshots():
    """Обработка скриншотов"""
    print("
=== ОБРАБОТКА СКРИНШОТОВ ===")
    
    screenshot_dir = 'screenshots'
    icon_dir = 'icons'
    
    # Проверяем наличие директорий
    if not os.path.exists(screenshot_dir):
        print(f"  ✗ Папка {screenshot_dir} не найдена")
        return
    
    if not os.path.exists(icon_dir):
        print(f"  ✗ Папка {icon_dir} не найдена")
        return
    
    # Считаем файлы
    screenshots = [f for f in os.listdir(screenshot_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    icons = [f for f in os.listdir(icon_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    print(f"  ✓ Найдено {len(screenshots)} скриншотов")
    print(f"  ✓ Найдено {len(icons)} иконок")
    
    # Показываем первые несколько скриншотов
    if screenshots:
        print("  Скриншоты:")
        for i, screenshot in enumerate(screenshots[:3]):
            print(f"    {i+1}. {screenshot}")
    
    if len(screenshots) > 3:
        print(f"  ... и еще {len(screenshots) - 3} файлов")

def main():
    """Главная функция"""
    print("=== СИСТЕМА ОБРАБОТКИ СКРИНШОТОВ ВЕНДОРА ===")
    
    # Проверяем наличие файлов
    if not check_files():
        print("  ⚠ Предупреждение: Не все необходимые файлы найдены")
    
    # Анализируем данные
    analyze_vendor_data()
    analyze_items_data()
    analyze_mapping()
    
    # Обрабатываем скриншоты
    process_screenshots()
    
    print("
=== РЕКОМЕНДАЦИИ ===")
    print("1. Для дальнейшей работы:")
    print("   - Проверьте содержимое vendor_data.txt")
    print("   - Убедитесь, что все данные корректны")
    print("   - Запустите vendor_screenshot_processor.py")
    print("2. Для улучшения:")
    print("   - Добавьте больше иконок в папку icons/")
    print("   - Проверьте mapping.json на полноту")
    print("   - Обновите vendor_data.txt при необходимости")

if __name__ == "__main__":
    main()
