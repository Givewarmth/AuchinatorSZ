import os
from PIL import Image

# Функция для сравнения изображений

def compare_images(screenshot_img, icon_img):
    # Простое сравнение пикселей
    pixels1 = screenshot_img.load()
    pixels2 = icon_img.load()
    
    width, height = screenshot_img.size
    total_diff = 0
    
    # Сравниваем пиксели по одному
    for y in range(height):
        for x in range(width):
            diff = abs(pixels1[x, y][0] - pixels2[x, y][0])
            total_diff += diff
    
    return total_diff

# Основной код

def main():
    # Пути к директориям
    screenshots_dir = "data/screenshots"
    icons_dir = "data/icons/bullet"
    
    # Получаем список файлов
    try:
        screenshots = [f for f in os.listdir(screenshots_dir) if f.endswith(".png")]
        icons = [f for f in os.listdir(icons_dir) if f.endswith(".png")]
        
        print("Сравнение с использованием простого анализа пикселей:")
        
        # Сравниваем каждое изображение
        for screenshot in screenshots:
            screenshot_path = os.path.join(screenshots_dir, screenshot)
            print(f"\nСкриншот: {screenshot}")
            
            # Открываем скриншот
            screenshot_img = Image.open(screenshot_path)
            
            # Сравниваем с каждой иконкой
            best_match = None
            best_similarity = float("inf")
            
            for icon in icons:
                icon_path = os.path.join(icons_dir, icon)
                icon_img = Image.open(icon_path)
                
                # Убедимся, что размеры совпадают
                if screenshot_img.size == icon_img.size:
                    diff = compare_images(screenshot_img, icon_img)
                    
                    if diff < best_similarity:
                        best_similarity = diff
                        best_match = icon
                        
                    print(f"  {icon}: разница = {diff}")
                else:
                    print(f"  {icon}: размеры не совпадают")
                
            print(f"  Лучший матч: {best_match} (разница = {best_similarity})")
    except Exception as e:
        print(f"Ошибка при чтении файлов: {e}")

if __name__ == "__main__":
    main()