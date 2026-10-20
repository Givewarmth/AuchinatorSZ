import cv2
import numpy as np
import os
from PIL import Image
import sys

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from screenshot_processor import ScreenshotProcessor


def test_screenshot_processing():
    """Тестирование обработки скриншотов"""
    print("Тестирование обработки скриншотов")
    
    # Создаем тестовый процессор
    processor = ScreenshotProcessor()
    
    # Проверяем, что директории существуют
    if not os.path.exists('screenshots'):
        print("Директория screenshots не существует")
        return
    
    if not os.path.exists('icons'):
        print("Директория icons не существует")
        return
    
    # Загружаем иконки
    processor.load_icons()
    print(f"Загружено иконок: {len(processor.icons)}")
    
    # Проверяем наличие скриншотов
    screenshot_files = os.listdir('screenshots')
    
    if not screenshot_files:
        print("Нет скриншотов для тестирования")
        return
    
    print(f"Найдено {len(screenshot_files)} скриншотов")
    
    # Пытаемся обработать первый скриншот
    try:
        first_screenshot = os.path.join('screenshots', screenshot_files[0])
        img = processor.process_screenshot(first_screenshot)
        print(f"Скриншот {screenshot_files[0]} успешно обработан")
        print(f"Размер изображения: {img.shape if img is not None else 'Не удалось загрузить'}")
    except Exception as e:
        print(f"Ошибка при обработке скриншота: {e}")
        
    print("Тест завершен")

if __name__ == "__main__":
    test_screenshot_processing()
    print("Тест обработки скриншотов завершен")
