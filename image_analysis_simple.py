# Импорт необходимых библиотек
import numpy as np
import os
from PIL import Image

# Функция для сравнения изображений
# Используем простое сравнение по пикселям
# Учитываем разницу в цветах

def compare_images(img1, img2):
    # Преобразование в массивы numpy
    img1_array = np.array(img1)
    img2_array = np.array(img2)
    
    # Приведение размеров к одному размеру
    # Если размеры не совпадают, мы будем использовать минимальный размер
    min_height = min(img1_array.shape[0], img2_array.shape[0])
    min_width = min(img1_array.shape[1], img2_array.shape[1])
    
    # Обрезаем изображения до минимального размера
    img1_array = img1_array[:min_height, :min_width]
    img2_array = img2_array[:min_height, :min_width]
    
    # Вычисление среднего квадрата разности (MSE)
    # Сначала преобразуем в float32 для точных вычислений
    img1_float = img1_array.astype(np.float32)
    img2_float = img2_array.astype(np.float32)
    
    # Вычисляем разность
    diff = img1_float - img2_float
    
    # Возводим в квадрат
    diff_squared = diff ** 2
    
    # Вычисляем среднее значение
    mse = np.mean(diff_squared)
    
    return mse

# Основная функция для анализа
# Вместо OpenCV используем PIL для работы с изображениями

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
                # Приводим изображения к одному размеру
                screenshot_resized = screenshot_img.resize((32, 32))
                icon_resized = icon_img.resize((32, 32))
                
                # Сравниваем
                mse = compare_images(screenshot_resized, icon_resized)
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