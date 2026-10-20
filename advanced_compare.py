import os
from PIL import Image
import numpy as np

def calculate_mse(image1, image2):
    """Вычисление среднеквадратичной ошибки (MSE)"""
    # Преобразуем изображения в массивы numpy
    img1_array = np.array(image1)
    img2_array = np.array(image2)
    
    # Вычисляем разность
    diff = img1_array.astype(np.float64) - img2_array.astype(np.float64)
    
    # Возводим в квадрат и находим среднее
    mse = np.mean(diff**2)
    
    return mse

def calculate_similarity(image1, image2):
    """Вычисление степени схожести изображений"""
    # Сравниваем размеры
    if image1.size != image2.size:
        return 0
    
    # Вычисляем MSE
    mse = calculate_mse(image1, image2)
    
    # Преобразуем MSE в степень схожести (чем меньше MSE, тем лучше схожесть)
    similarity = 1 / (1 + mse)
    
    return similarity

def main():
    # Пути к директориям
    screenshots_dir = "data/screenshots"
    icons_dir = "data/icons/bullet"
    
    # Получаем список файлов
    try:
        screenshots = [f for f in os.listdir(screenshots_dir) if f.endswith(".png")]
        icons = [f for f in os.listdir(icons_dir) if f.endswith(".png")]
        
        print("Сравнение с использованием MSE и степени схожести:")
        
        # Сравниваем каждое изображение
        for screenshot in screenshots:
            screenshot_path = os.path.join(screenshots_dir, screenshot)
            print(f"\nСкриншот: {screenshot}")
            
            # Открываем скриншот
            screenshot_img = Image.open(screenshot_path)
            
            # Сравниваем с каждой иконкой
            best_match = None
            best_similarity = 0
            
            for icon in icons:
                icon_path = os.path.join(icons_dir, icon)
                icon_img = Image.open(icon_path)
                
                # Вычисляем степень схожести
                similarity = calculate_similarity(screenshot_img, icon_img)
                
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = icon
                    
                print(f"  {icon}: схожесть = {similarity:.6f}")
            
            print(f"  Лучший матч: {best_match} (схожесть = {best_similarity:.6f})")
    except Exception as e:
        print(f"Ошибка при чтении файлов: {e}")

if __name__ == "__main__":
    main()