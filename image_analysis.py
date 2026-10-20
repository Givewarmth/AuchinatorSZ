import os
import numpy as np
from PIL import Image


def load_image(path):
    try:
        return Image.open(path)
    except:
        return None


def resize_image(img, target_size=(32, 32)):
    # Масштабируем изображение до целевого размера
    if img is not None:
        return img.resize(target_size, Image.LANCZOS)
    return None


def calculate_mse(img1, img2):
    # Преобразуем изображения в массивы numpy
    if img1 is None or img2 is None:
        return float('inf')
    
    # Преобразуем в градации серого
    if len(img1.shape) == 3:
        img1 = np.dot(img1[...,:3], [0.2989, 0.5870, 0.1140])
    if len(img2.shape) == 3:
        img2 = np.dot(img2[...,:3], [0.2989, 0.5870, 0.1140])
    
    # Выравниваем размеры
    if img1.shape != img2.shape:
        # Если размеры разные, масштабируем до одного размера
        # В данном случае мы просто возвращаем высокую ошибку
        return float('inf')
    
    # Вычисляем MSE
    mse = np.mean((img1.astype("float") - img2.astype("float")) ** 2)
    return mse


def main():
    # Проверяем существование директорий
    screenshots_dir = "data/screenshots"
    icons_dir = "data/icons/bullet"
    
    if not os.path.exists(screenshots_dir) or not os.path.exists(icons_dir):
        print("Одна или обе директории не существуют")
        return
    
    # Получаем список файлов
    screenshot_files = [f for f in os.listdir(screenshots_dir) if f.endswith(".png")]
    icon_files = [f for f in os.listdir(icons_dir) if f.endswith(".png")]
    
    print("Сравнение файлов:")
    
    # Сравниваем каждый скриншот с каждой иконкой
    for screenshot in screenshot_files:
        screenshot_path = os.path.join(screenshots_dir, screenshot)
        
        for icon in icon_files:
            icon_path = os.path.join(icons_dir, icon)
            
            # Загружаем изображения
            img1 = load_image(screenshot_path)
            img2 = load_image(icon_path)
            
            # Масштабируем до одинакового размера
            img1_resized = resize_image(img1)
            img2_resized = resize_image(img2)
            
            if img1_resized is not None and img2_resized is not None:
                # Преобразуем в numpy массивы
                img1_array = np.array(img1_resized)
                img2_array = np.array(img2_resized)
                
                mse = calculate_mse(img1_array, img2_array)
                
                if mse == float('inf'):
                    print(f'{screenshot} vs {icon}: Невозможно сравнить (разные размеры)')
                else:
                    print(f'{screenshot} vs {icon}: MSE = {mse:.4f}')
            else:
                print(f'{screenshot} vs {icon}: Ошибка загрузки изображения')

if __name__ == "__main__":
    main()