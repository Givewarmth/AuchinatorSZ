# Анализ изображений без внешних библиотек
import os
from PIL import Image
import math

# Функция для сравнения изображений по пикселям
# Используем простую реализацию без numpy

def compare_images(img1, img2):
    # Получаем размеры изображений
    width1, height1 = img1.size
    width2, height2 = img2.size
    
    # Определяем минимальные размеры
    min_width = min(width1, width2)
    min_height = min(height1, height2)
    
    # Приводим размеры к 32x32
    img1 = img1.resize((32, 32))
    img2 = img2.resize((32, 32))
    
    # Считаем MSE
    total_diff = 0
    count = 0
    
    # Проходим по пикселям
    for y in range(32):
        for x in range(32):
            # Получаем цвета пикселей
            pixel1 = img1.getpixel((x, y))
            pixel2 = img2.getpixel((x, y))
            
            # Для RGB изображений у нас 3 компонента
            if isinstance(pixel1, tuple) and isinstance(pixel2, tuple):
                # Сравниваем каждую компоненту
                for i in range(len(pixel1)):
                    diff = pixel1[i] - pixel2[i]
                    total_diff += diff * diff
                    count += 1
            else:
                # Для градации серого
                diff = pixel1 - pixel2
                total_diff += diff * diff
                count += 1
    
    # Возвращаем среднее значение
    if count > 0:
        return total_diff / count
    else:
        return float('inf')

# Основная функция для анализа
# Используем только стандартные библиотеки

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
        screenshots[file] = Image.open(path)
        
    # Загрузка иконок
    icons = {}
    for file in icon_files:
        path = os.path.join(icons_dir, file)
        icons[file] = Image.open(path)
        
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
                # Сравниваем
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