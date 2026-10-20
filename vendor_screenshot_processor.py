
"""
Обработка скриншотов для вендора
"""

import os
import cv2
import numpy as np
from pathlib import Path
import json

def load_mapping():
    """Загрузка сопоставления иконок"""
    try:
        with open('mapping.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def load_vendor_data():
    """Загрузка данных вендора"""
    try:
        with open('vendor_data.txt', 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return []

def process_screenshot(screenshot_path):
    """Обработка одного скриншота"""
    print(f"Обработка скриншота: {screenshot_path}")
    
    # Загрузка изображения
    try:
        image = cv2.imread(screenshot_path)
        if image is None:
            print(f"  ❌ Не удалось загрузить изображение: {screenshot_path}")
            return None
            
        # Получаем размеры
        height, width = image.shape[:2]
        print(f"  Размер: {width}x{height}")
        
        # Определяем области для анализа
        # Пример: анализ центральной области для поиска предметов
        center_x = width // 2
        center_y = height // 2
        
        # Для примера - анализ центральной области 100x100 пикселей
        crop_size = 100
        y_start = max(0, center_y - crop_size // 2)
        y_end = min(height, center_y + crop_size // 2)
        x_start = max(0, center_x - crop_size // 2)
        x_end = min(width, center_x + crop_size // 2)
        
        cropped = image[y_start:y_end, x_start:x_end]
        
        # Сохраняем обработанную область
        output_path = f"processed_{os.path.basename(screenshot_path)}"
        cv2.imwrite(output_path, cropped)
        print(f"  ✓ Сохранено обработанное изображение: {output_path}")
        
        return cropped
        
    except Exception as e:
        print(f"  ❌ Ошибка при обработке: {e}")
        return None

def analyze_screenshot_with_icons(screenshot_path, icons_dir):
    """Анализ скриншота с использованием иконок"""
    print(f"Анализ скриншота с иконками: {screenshot_path}")
    
    # Загрузка иконок
    icon_files = [f for f in os.listdir(icons_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    print(f"  Найдено {len(icon_files)} иконок для сравнения")
    
    # Загрузка скриншота
    image = cv2.imread(screenshot_path)
    if image is None:
        print(f"  ❌ Не удалось загрузить скриншот: {screenshot_path}")
        return None
    
    # Простой поиск иконок (в реальном приложении здесь будет сложный алгоритм)
    results = []
    for icon_file in icon_files[:3]:  # Проверяем первые 3 иконки
        icon_path = os.path.join(icons_dir, icon_file)
        try:
            icon = cv2.imread(icon_path)
            if icon is not None:
                # Упрощенный поиск - просто сравнение размеров
                icon_height, icon_width = icon.shape[:2]
                image_height, image_width = image.shape[:2]
                
                print(f"    Иконка {icon_file}: {icon_width}x{icon_height}")
                print(f"    Скриншот: {image_width}x{image_height}")
                
                # Проверяем, что иконка не больше скриншота
                if icon_height <= image_height and icon_width <= image_width:
                    results.append(f"  ✓ Сопоставление: {icon_file}")
                else:
                    results.append(f"  ⚠ Размер не совпадает: {icon_file}")
                    
        except Exception as e:
            print(f"    ❌ Ошибка при анализе иконки {icon_file}: {e}")
    
    return results

def main():
    """Главная функция"""
    print("=== ОБРАБОТКА СКРИНШОТОВ ВЕНДОРА ===")
    
    # Проверяем директории
    screenshots_dir = 'screenshots'
    icons_dir = 'icons'
    
    if not os.path.exists(screenshots_dir):
        print(f"❌ Папка {screenshots_dir} не найдена")
        return
    
    if not os.path.exists(icons_dir):
        print(f"❌ Папка {icons_dir} не найдена")
        return
    
    # Получаем список скриншотов
    screenshots = [f for f in os.listdir(screenshots_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    print(f"Найдено {len(screenshots)} скриншотов для обработки:")
    
    # Обрабатываем каждый скриншот
    for i, screenshot in enumerate(screenshots, 1):
        screenshot_path = os.path.join(screenshots_dir, screenshot)
        print(f"
{i}. {screenshot}")
        
        # Обработка скриншота
        processed = process_screenshot(screenshot_path)
        
        # Анализ с иконками
        if processed is not None:
            analysis = analyze_screenshot_with_icons(screenshot_path, icons_dir)
            if analysis:
                for result in analysis:
                    print(result)
    
    print("
=== ЗАВЕРШЕНИЕ ===")
    print("Обработка скриншотов завершена.")

if __name__ == "__main__":
    main()
