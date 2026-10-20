import os
import numpy as np
from PIL import Image


def load_image(image_path):
    try:
        # Загружаем изображение с помощью PIL
        img = Image.open(image_path)
        return np.array(img)
    except Exception as e:
        print(f"Ошибка при загрузке изображения {image_path}: {e}")
        return None


def find_objects_by_comparison(img_path, template_path, threshold=0.7):
    # Загружаем изображение и шаблон
    img = load_image(img_path)
    template = load_image(template_path)
    
    if img is None or template is None:
        return []
    
    # Преобразуем в оттенки серого
    if len(img.shape) == 3:
        img_gray = np.dot(img[...,:3], [0.2989, 0.5870, 0.1140])
    else:
        img_gray = img
    
    if len(template.shape) == 3:
        template_gray = np.dot(template[...,:3], [0.2989, 0.5870, 0.1140])
    else:
        template_gray = template
    
    # Проверяем размеры
    if template_gray.shape[0] > img_gray.shape[0] or template_gray.shape[1] > img_gray.shape[1]:
        print("Размер шаблона превышает размер изображения")
        return []
    
    # Поиск объектов
    positions = []
    
    # Простая проверка на соответствие
    for i in range(img_gray.shape[0] - template_gray.shape[0]):
        for j in range(img_gray.shape[1] - template_gray.shape[1]):
            # Сравниваем участки
            patch = img_gray[i:i+template_gray.shape[0], j:j+template_gray.shape[1]]
            
            # Считаем среднее значение
            avg = np.mean(patch)
            
            # Сравниваем с шаблоном
            if abs(avg - np.mean(template_gray)) > threshold * 100:
                positions.append((j, i))
    
    return positions


def find_all_objects(image_path, template_paths, threshold=0.7):
    all_positions = []
    
    for i, template_path in enumerate(template_paths):
        print(f"Поиск объектов с шаблоном {i+1}")
        
        positions = find_objects_by_comparison(image_path, template_path, threshold)
        all_positions.extend(positions)
        
        print(f"Найдено {len(positions)} объектов")
        
    return all_positions


def main():
    # Путь к изображению
    image_path = "image.png"  # Замените на реальный путь
    
    # Пути к шаблонам
    template_paths = ["template1.png", "template2.png"]  # Замените на реальные пути
    
    # Анализ изображения
    positions = find_all_objects(image_path, template_paths)
    
    print(f"Общее количество найденных объектов: {len(positions)}")
    
    for i, (x, y) in enumerate(positions):
        print(f"Объект {i+1}: ({x}, {y})")


if __name__ == "__main__":
    main()'}]