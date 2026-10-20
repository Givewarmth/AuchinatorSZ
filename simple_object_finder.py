import os
import cv2
import numpy as np


def load_image(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            print(f"Не удалось загрузить изображение: {image_path}")
            return None
        return img
    except Exception as e:
        print(f"Ошибка при загрузке изображения {image_path}: {e}")
        return None


def find_objects_by_template(img_path, template_path, threshold=0.7):
    # Загружаем изображение и шаблон
    img = load_image(img_path)
    template = load_image(template_path)
    
    if img is None or template is None:
        return []
    
    # Конвертируем в оттенки серого
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    
    # Поиск с помощью шаблонного сопоставления
    result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    
    # Находим все позиции, где значение больше порога
    locations = np.where(result >= threshold)
    positions = list(zip(*locations[::-1]))
    
    return positions


def find_all_objects(image_path, template_paths, threshold=0.7):
    all_positions = []
    
    for i, template_path in enumerate(template_paths):
        print(f"Поиск объектов с шаблоном {i+1}")
        
        positions = find_objects_by_template(image_path, template_path, threshold)
        all_positions.extend(positions)
        
        print(f"Найдено {len(positions)} объектов")
        
    return all_positions


def analyze_image(image_path, template_paths):
    print(f"Анализ изображения: {image_path}")
    
    # Проверяем существование файлов
    if not os.path.exists(image_path):
        print(f"Файл изображения не существует: {image_path}")
        return []
    
    all_positions = []
    
    for i, template_path in enumerate(template_paths):
        if not os.path.exists(template_path):
            print(f"Файл шаблона не существует: {template_path}")
            continue
        
        print(f"Анализ шаблона {i+1}: {template_path}")
        
        positions = find_objects_by_template(image_path, template_path)
        all_positions.extend(positions)
        
        print(f"Найдено {len(positions)} объектов")
    
    return all_positions


def main():
    # Путь к изображению
    image_path = "image.png"  # Замените на реальный путь
    
    # Пути к шаблонам
    template_paths = ["template1.png", "template2.png"]  # Замените на реальные пути
    
    # Анализ изображения
    positions = analyze_image(image_path, template_paths)
    
    print(f"Общее количество найденных объектов: {len(positions)}")
    
    for i, (x, y) in enumerate(positions):
        print(f"Объект {i+1}: ({x}, {y})")


if __name__ == "__main__":
    main()