import os
import json
from PIL import Image
import numpy as np

def load_mapping():
    """Загружает файл mapping.json"""
    try:
        with open('mapping.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Файл mapping.json не найден")
        return None

def compare_screenshots_with_icons():
    """Сравнивает скриншоты с иконками"""
    mapping = load_mapping()
    
    if not mapping:
        return
    
    # Путь к скриншотам
    screenshots_path = mapping.get('screenshots', {}).get('path', '')
    
    # Путь к иконкам
    icons_path = mapping.get('items', {}).get('weapon', {}).get('icon_path', '')
    
    print(f"Путь к скриншотам: {screenshots_path}")
    print(f"Путь к иконкам: {icons_path}")
    
    # Проверяем существование папок
    if not os.path.exists(screenshots_path):
        print(f"Папка скриншотов не существует: {screenshots_path}")
        return
    
    # Получаем список скриншотов
    screenshot_files = []
    try:
        for file in os.listdir(screenshots_path):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                screenshot_files.append(file)
    except Exception as e:
        print(f"Ошибка чтения скриншотов: {e}")
        return
    
    print(f"Найдено скриншотов: {len(screenshot_files)}")
    
    # Для демонстрации - выводим информацию о скриншотах
    for file in screenshot_files:
        print(f"Скриншот: {file}")
    
    # Проверяем иконки
    icons_dir = os.path.dirname(icons_path)
    print(f"Папка иконок: {icons_dir}")
    
    if os.path.exists(icons_dir):
        try:
            icon_files = os.listdir(icons_dir)
            print(f"Найдено иконок: {len(icon_files)}")
            for icon in icon_files:
                print(f"Иконка: {icon}")
        except Exception as e:
            print(f"Ошибка чтения иконок: {e}")
    else:
        print(f"Папка иконок не существует: {icons_dir}")

# Основная функция
if __name__ == "__main__":
    compare_screenshots_with_icons()
