import os
import cv2
import numpy as np
from PIL import Image

# Функция для вычисления MSE (Mean Squared Error)
def calculateMSE(image1, image2):
    # Убедимся, что изображения имеют одинаковый размер
    if image1.shape != image2.shape:
        print(f"Размеры изображений не совпадают: {image1.shape} vs {image2.shape}")
        return None
    
    # Вычисляем разность между изображениями
    diff = cv2.subtract(image1, image2)
    # Возводим разность в квадрат
    squared_diff = np.square(diff)
    # Находим среднее значение квадратов разности
    mse = np.mean(squared_diff)
    return mse

# Функция для сравнения изображений
def compare_images(image1, image2):
    # Проверяем, совпадают ли размеры изображений
    if image1.shape == image2.shape:
        mse = calculateMSE(image1, image2)
        return mse
    else:
        print("Размеры изображений не совпадают")
        return None

# Функция для загрузки и анализа изображений
def load_and_analyze_image(image_path):
    try:
        # Загружаем изображение с помощью OpenCV
        img = cv2.imread(image_path)
        if img is None:
            print(f"Ошибка загрузки изображения: {image_path}")
            return None
        return img
    except Exception as e:
        print(f"Ошибка при загрузке изображения {image_path}: {e}")
        return None

# Путь к папкам с данными
screenshots_dir = "data/screenshots"
icons_dir = "data/icons/bullet"

# Считываем список скриншотов и иконок
screenshots = os.listdir(screenshots_dir)
icons = os.listdir(icons_dir)

print("Сравнение с использованием анализа пикселей:")

# Загружаем скриншоты и иконки
screenshots_images = []
icons_images = []

for screenshot in screenshots:
    screenshot_path = os.path.join(screenshots_dir, screenshot)
    screenshot_img = load_andalyze_image(screenshot_path)
    if screenshot_img is not None:
        screenshots_images.append(screenshot_img)
        print(f"Успешно загружен скриншот: {screenshot}")
    else:
        print(f"Ошибка загрузки скриншота: {screenshot}")
    
for icon in icons:
    icon_path = os.path.join(icons_dir, icon)
    icon_img = load_and_analyze_image(icon_path)
    if icon_img is not None:
        icons_images.append(icon_img)
        print(f"Успешно загружена иконка: {icon}")
    else:
        print(f"Ошибка загрузки иконки: {icon}")
    
# Сравниваем скриншоты с иконками
print("Начинаем сравнение:")
for i, screenshot_img in enumerate(screenshots_images):
    print(f"Сравнение скриншота {i+1}:")
    for j, icon_img in enumerate(icons_images):
        if screenshot_img is not None and icon_img is not None:
            mse = compare_images(screenshot_img, icon_img)
            if mse is not None:
                print(f"  Иконка {j+1}: MSE = {mse}")
            else:
                print(f"  Иконка {j+1}: Ошибка сравнения")
        else:
            print(f"  Иконка {j+1}: Ошибка загрузки изображения")
            
print("Анализ завершен.")