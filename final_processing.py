
import os
import json
from PIL import Image
import numpy as np

def calculate_mse(image1, image2):
    """Вычисляет среднеквадратичную ошибку между двумя изображениями"""
    try:
        # Преобразуем изображения в массивы numpy
        array1 = np.array(image1)
        array2 = np.array(image2)
        
        # Убедимся, что массивы одинакового размера
        min_height = min(array1.shape[0], array2.shape[0])
        min_width = min(array1.shape[1], array2.shape[1])
        
        # Обрезаем до минимального размера
        array1 = array1[:min_height, :min_width]
        array2 = array2[:min_height, :min_width]
        
        # Вычисляем разность и возводим в квадрат
        mse = np.mean((array1.astype(float) - array2.astype(float)) ** 2)
        return mse
    except Exception as e:
        print(f"Ошибка в вычислении MSE: {e}")
        return None

def compare_images(screenshot_path, item_path):
    """Сравнивает скриншот с иконкой"""
    try:
        # Открываем изображения
        screenshot = Image.open(screenshot_path)
        item = Image.open(item_path)
        
        # Преобразуем в RGB если нужно
        if screenshot.mode != 'RGB':
            screenshot = screenshot.convert('RGB')
        if item.mode != 'RGB':
            item = item.convert('RGB')
            
        # Вычисляем MSE
        mse = calculate_mse(screenshot, item)
        return mse
    except Exception as e:
        print(f"Ошибка при сравнении {screenshot_path} и {item_path}: {e}")
        return None

def process_screenshots():
    """Обрабатывает скриншоты и ищет их в папке items"""
    screenshots_dir = "sandbox/data/screenshots"
    items_dir = "sandbox/data/items"
    output_file = "screenshots_results.json"
    
    results = {}
    
    # Проверяем существование директорий
    if not os.path.exists(screenshots_dir):
        print(f"Директория скриншотов не найдена: {screenshots_dir}")
        return
    
    if not os.path.exists(items_dir):
        print(f"Директория иконок не найдена: {items_dir}")
        return
    
    # Получаем список скриншотов
    screenshots = [f for f in os.listdir(screenshots_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not screenshots:
        print("В директории скриншотов не найдено файлов")
        return
    
    print(f"Найдено {len(screenshots)} скриншотов")
    
    # Проходим по каждому скриншоту
    for screenshot in screenshots:
        screenshot_path = os.path.join(screenshots_dir, screenshot)
        print(f"Обрабатываем скриншот: {screenshot}")
        
        # Ищем соответствующую иконку
        item_name = os.path.splitext(screenshot)[0]  # Имя файла без расширения
        item_path = os.path.join(items_dir, f"{item_name}.png")
        
        # Проверяем, существует ли иконка
        if os.path.exists(item_path):
            mse = compare_images(screenshot_path, item_path)
            if mse is not None:
                results[screenshot] = {
                    "item": f"{item_name}.png",
                    "mse": float(mse)
                }
                print(f"  Сравнено с {item_name}.png, MSE: {mse}")
            else:
                results[screenshot] = {
                    "item": f"{item_name}.png",
                    "mse": None
                }
                print(f"  Ошибка сравнения с {item_name}.png")
        else:
            print(f"  Иконка {item_name}.png не найдена в папке items")
            results[screenshot] = {
                "item": None,
                "mse": None
            }
    
    # Сохраняем результаты
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Результаты сохранены в {output_file}")
    return results

def main():
    """Главная функция"""
    print("=== Финальный скрипт обработки скриншотов ===")
    print("Проверяем структуру данных...")
    
    # Проверяем существование необходимых директорий
    screenshots_dir = "sandbox/data/screenshots"
    items_dir = "sandbox/data/items"
    
    if not os.path.exists(screenshots_dir):
        print(f"Директория скриншотов не найдена: {screenshots_dir}")
        return
    
    if not os.path.exists(items_dir):
        print(f"Директория иконок не найдена: {items_dir}")
        return
    
    # Обрабатываем скриншоты
    results = process_screenshots()
    
    if results:
        print("Результаты обработки:")
        for screenshot, data in results.items():
            print(f"  {screenshot}: {data}")
    else:
        print("Нет результатов для отображения")

if __name__ == "__main__":
    main()
