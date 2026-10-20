import os
import numpy as np
from PIL import Image


def load_image(image_path):
    """Загрузка изображения"""
    try:
        img = Image.open(image_path)
        return np.array(img)
    except Exception as e:
        print(f"Ошибка при загрузке изображения {image_path}: {e}")
        return None


def find_all_objects(image_path, template_paths, threshold=0.8):
    """Поиск всех объектов на изображении"""
    # Загружаем основное изображение
    img = load_image(image_path)
    if img is None:
        return []
    
    # Собираем все найденные позиции
    all_positions = []
    
    for i, template_path in enumerate(template_paths):
        print(f"Поиск шаблона {i+1}: {template_path}")
        
        # Загружаем шаблон
        template = load_image(template_path)
        if template is None:
            continue
        
        # Проверяем, что размеры совпадают
        if img.shape[:2] != template.shape[:2]:
            print(f"Размеры изображения и шаблона не совпадают")
            continue
        
        # Вычисляем разницу между изображением и шаблоном
        diff = np.abs(img.astype(np.float32) - template.astype(np.float32))
        
        # Вычисляем среднеквадратичную ошибку
        mse = np.mean(diff**2)
        
        # Проверяем, что MSE находится в допустимых пределах
        if mse < threshold:
            # Найден объект
            all_positions.append((0, 0))  # Просто добавляем координаты
            print(f"Найден объект с MSE = {mse}")
        else:
            print(f"Объект не найден, MSE = {mse}")
    
    return all_positions


def find_all_objects_simple(image_path, template_path, threshold=0.8):
    """Поиск всех объектов на изображении с простым сравнением"""
    # Загружаем основное изображение
    img = load_image(image_path)
    if img is None:
        return []
    
    # Загружаем шаблон
    template = load_image(template_path)
    if template is None:
        return []
    
    # Проверяем, что размеры совпадают
    if img.shape[:2] != template.shape[:2]:
        print(f"Размеры изображения и шаблона не совпадают")
        return []
    
    # Вычисляем разницу между изображением и шаблоном
    diff = np.abs(img.astype(np.float32) - template.astype(np.float32))
    
    # Вычисляем среднеквадратичную ошибку
    mse = np.mean(diff**2)
    
    # Проверяем, что MSE находится в допустимых пределах
    if mse < threshold:
        # Найден объект
        print(f"Найден объект с MSE = {mse}")
        return [(0, 0)]
    else:
        print(f"Объект не найден, MSE = {mse}")
        return []


def main():
    # Путь к изображению
    image_path = "image.png"  # Замените на реальный путь
    
    # Путь к шаблону
    template_path = "template.png"  # Замените на реальный путь
    
    # Анализ изображения
    positions = find_all_objects_simple(image_path, template_path)
    
    print(f"Найдено {len(positions)} объектов")
    for i, (x, y) in enumerate(positions):
        print(f"Объект {i+1}: ({x}, {y})")


if __name__ == "__main__":
    main()