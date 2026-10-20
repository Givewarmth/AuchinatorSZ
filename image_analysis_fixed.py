# Импорт необходимых библиотек
import cv2
import numpy as np
import os
from pathlib import Path

# Функция для сравнения изображений
def compare_images(img1, img2):
    # Приведение размеров изображений к одному размеру
    img1 = cv2.resize(img1, (32, 32))
    img2 = cv2.resize(img2, (32, 32))
    
    # Преобразование в оттенки серого
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Вычисление среднего квадрата разности (MSE)
    mse = np.mean((img1.astype(np.float32) - img2.astype(np.float32)) ** 2)
    return mse

# Основная функция для анализа
def analyze_images():
    # Путь к папке с скриншотами
    screenshots_dir = 'data/screenshots'
    
    # Путь к папке с иконками
    icons_dir = 'data/icons/bullet'
    
    # Получение списка скриншотов
    screenshot_files = [f for f in os.listdir(screenshots_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    # Получение списка иконок
    icon_files = [f for f in os.listdir(icons_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    # Создание словаря для хранения результатов
    results = {}
    
    # Загрузка скриншотов
    screenshots = {}
    for file in screenshot_files:
        path = os.path.join(screenshots_dir, file)
        screenshots[file] = cv2.imread(path)
        
    # Загрузка иконок
    icons = {}
    for file in icon_files:
        path = os.path.join(icons_dir, file)
        icons[file] = cv2.imread(path)
        
    # Сравнение скриншотов с иконками
    for screenshot_file in screenshot_files:
        print(f'Анализ скриншота: {screenshot_file}')
        
        # Получение изображения скриншота
        screenshot_img = screenshots[screenshot_file]
        
        # Сравнение с каждой иконкой
        scores = []
        for icon_file in icon_files:
            icon_img = icons[icon_file]
            
            # Проверка, что изображения загружены
            if screenshot_img is not None and icon_img is not None:
                mse = compare_images(screenshot_img, icon_img)
                scores.append((icon_file, mse))
            
        # Сортировка по значению MSE
        scores.sort(key=lambda x: x[1])
        
        # Вывод топ-5 результатов
        results[screenshot_file] = scores[:5]
        
        for i, (icon_file, mse) in enumerate(scores[:5]):
            print(f'  {i+1}. {icon_file} (MSE: {mse:.2f})')
        
    return results

# Запуск анализа
if __name__ == "__main__":
    analyze_images()