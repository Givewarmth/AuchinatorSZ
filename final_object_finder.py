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

def find_all_objects(image_path, template_paths, threshold=0.7):
    all_positions = []
    
    # Загружаем изображение
    img = load_image(image_path)
    if img is None:
        return []
    
    # Преобразуем в оттенки серого
    if len(img.shape) == 3:
        img_gray = np.dot(img[...,:3], [0.2989, 0.5870, 0.1140])
    else:
        img_gray = img
    
    for i, template_path in enumerate(template_paths):
        print(f"Поиск объектов с шаблоном {i+1}")
        
        # Загружаем шаблон
        template = load_image(template_path)
        if template is None:
            continue
        
        # Преобразуем шаблон в оттенки серого
        if len(template.shape) == 3:
            template_gray = np.dot(template[...,:3], [0.2989, 0.5870, 0.1140])
        else:
            template_gray = template
        
        # Проверяем размеры
        if template_gray.shape[0] > img_gray.shape[0] or template_gray.shape[1] > img_gray.shape[1]:
            print("Размер шаблона превышает размер изображения")
            continue
        
        # Поиск объектов с помощью шаблонного сопоставления
        positions = []
        
        # Сравниваем по всем позициям
        for i in range(img_gray.shape[0] - template_gray.shape[0]):
            for j in range(img_gray.shape[1] - template_gray.shape[1]):
                # Берем участок изображения
                patch = img_gray[i:i+template_gray.shape[0], j:j+template_gray.shape[1]]
                
                # Сравниваем с шаблоном
                if abs(np.mean(patch) - np.mean(template_gray)) < threshold * 100:
                    positions.append((j, i))
        
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
    main()