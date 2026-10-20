import cv2
import numpy as np
from PIL import Image
import os


def load_image(image_path):
    """Загрузка изображения"""
    try:
        # Загружаем изображение с помощью OpenCV
        img = cv2.imread(image_path)
        if img is None:
            print(f"Не удалось загрузить изображение: {image_path}")
            return None
        # Преобразуем BGR в RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img
    except Exception as e:
        print(f"Ошибка при загрузке изображения {image_path}: {e}")
        return None


def find_all_objects(image_path, template_path, threshold=0.8):
    """Поиск всех объектов на изображении с использованием шаблонного соответствия"""
    # Загружаем основное изображение
    img = load_image(image_path)
    if img is None:
        return []
    
    # Загружаем шаблон
    template = load_image(template_path)
    if template is None:
        return []
    
    # Конвертируем в оттенки серого
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
    
    # Поиск соответствия
    result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    
    # Находим все позиции с высоким уровнем соответствия
    locations = np.where(result >= threshold)
    positions = list(zip(*locations[::-1]))
    
    return positions


def analyze_image(image_path, template_paths, threshold=0.8):
    """Анализ изображения с поиском всех объектов"""
    print(f"Анализ изображения: {image_path}")
    
    # Проверяем, существует ли файл изображения
    if not os.path.exists(image_path):
        print(f"Файл изображения не существует: {image_path}")
        return []
    
    # Собираем все найденные позиции
    all_positions = []
    
    for i, template_path in enumerate(template_paths):
        print(f"Поиск шаблона {i+1}: {template_path}")
        
        # Проверяем, существует ли файл шаблона
        if not os.path.exists(template_path):
            print(f"Файл шаблона не существует: {template_path}")
            continue
        
        # Находим все объекты
        positions = find_all_objects(image_path, template_path, threshold)
        all_positions.extend(positions)
        
        print(f"Найдено {len(positions)} объектов")
    
    return all_positions

# Пример использования
if __name__ == "__main__":
    # Путь к изображению
    image_path = "image.png"  # Замените на реальный путь
    
    # Пути к шаблонам (можно добавить несколько шаблонов)
    template_paths = ["template1.png", "template2.png"]  # Замените на реальные пути
    
    # Анализ изображения
    positions = analyze_image(image_path, template_paths)
    
    print(f"Найдено {len(positions)} объектов")
    for i, (x, y) in enumerate(positions):
        print(f"Объект {i+1}: ({x}, {y})")