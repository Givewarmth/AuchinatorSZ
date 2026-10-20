import os
import sys
from PIL import Image
import numpy as np

# Добавляем текущую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from icon_data_handler import get_icon_files, get_screenshot_files


def compare_images(image1_path, image2_path):
    """Сравнение двух изображений"""
    try:
        # Загрузка изображений
        img1 = Image.open(image1_path)
        img2 = Image.open(image2_path)
        
        # Преобразование в numpy массивы
        arr1 = np.array(img1)
        arr2 = np.array(img2)
        
        # Проверка размеров
        if arr1.shape != arr2.shape:
            print(f"Разные размеры: {arr1.shape} vs {arr2.shape}")
            return None
        
        # Вычисление разности
        diff = np.abs(arr1.astype(np.float64) - arr2.astype(np.float64))
        
        # Среднее значение разности
        avg_diff = np.mean(diff)
        
        return avg_diff
    except Exception as e:
        print(f"Ошибка при сравнении изображений: {e}")
        return None


def compare_screenshots_with_icons():
    """Сравнение скриншотов с иконками"""
    print("Сравнение скриншотов с иконками")
    
    # Получение файлов
    screenshot_files = get_screenshot_files()
    icon_files = get_icon_files()
    
    if not screenshot_files:
        print("Нет скриншотов для сравнения")
        return
    
    if not icon_files:
        print("Нет иконок для сравнения")
        return
    
    print(f"Найдено {len(screenshot_files)} скриншотов и {len(icon_files)} иконок")
    
    # Сравнение каждого скриншота с каждой иконкой
    for i, screenshot in enumerate(screenshot_files):
        print(f"\nСкриншот {i+1}: {os.path.basename(screenshot)}")
        
        for j, icon in enumerate(icon_files):
            print(f"  Сравнение с иконкой {j+1}: {os.path.basename(icon)}")
            
            # Выполнение сравнения
            diff = compare_images(screenshot, icon)
            
            if diff is not None:
                print(f"    Средняя разница: {diff:.2f}")
            else:
                print("    Ошибка сравнения")
                
    print("\nСравнение завершено")


def main():
    compare_screenshots_with_icons()

if __name__ == "__main__":
    main()