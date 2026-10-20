"""
Обработка скриншотов и сравнение с иконками
"""

import cv2
import numpy as np
from PIL import Image
import os

def load_icon(icon_path):
    """Загрузка иконки из файла"""
    try:
        icon = cv2.imread(icon_path)
        if icon is None:
            print(f"Ошибка: Не удалось загрузить иконку {icon_path}")
            return None
        return icon
    except Exception as e:
        print(f"Ошибка при загрузке иконки {icon_path}: {e}")
        return None

def compare_screenshot_with_icon(screenshot_path, icon_path, threshold=0.8):
    """Сравнение скриншота с иконкой"""
    try:
        # Загрузка скриншота
        screenshot = cv2.imread(screenshot_path)
        if screenshot is None:
            print(f"Ошибка: Не удалось загрузить скриншот {screenshot_path}")
            return None
        
        # Загрузка иконки
        icon = load_icon(icon_path)
        if icon is None:
            return None
        
        # Приведение размеров к одному размеру (если нужно)
        screenshot_resized = cv2.resize(screenshot, (icon.shape[1], icon.shape[0]))
        
        # Конвертация в оттенки серого для сравнения
        screenshot_gray = cv2.cvtColor(screenshot_resized, cv2.COLOR_BGR2GRAY)
        icon_gray = cv2.cvtColor(icon, cv2.COLOR_BGR2GRAY)
        
        # Сравнение с порогом
        similarity = np.sum(screenshot_gray == icon_gray) / (screenshot_gray.shape[0] * screenshot_gray.shape[1])
        
        # Возвращаем результат сравнения
        return similarity >= threshold
        
    except Exception as e:
        print(f"Ошибка при сравнении: {e}")
        return None

def process_screenshots(icon_folder, screenshot_folder, output_folder):
    """Обработка всех скриншотов в папке"""
    # Создаем папку для вывода, если она не существует
    os.makedirs(output_folder, exist_ok=True)
    
    # Получаем список всех скриншотов
    screenshot_files = [f for f in os.listdir(screenshot_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    results = {}
    for screenshot_file in screenshot_files:
        screenshot_path = os.path.join(screenshot_folder, screenshot_file)
        print(f"Обрабатываем скриншот: {screenshot_file}")
        
        # Для каждой иконки в папке
        icon_files = [f for f in os.listdir(icon_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        matches = []
        
        for icon_file in icon_files:
            icon_path = os.path.join(icon_folder, icon_file)
            match = compare_screenshot_with_icon(screenshot_path, icon_path)
            if match is True:
                matches.append(icon_file)
        
        results[screenshot_file] = matches
    
    return results

if __name__ == "__main__":
    # Пример использования
    print("Обработка скриншотов...")
    # Здесь можно добавить конкретную логику для запуска
    print("Готово.")
