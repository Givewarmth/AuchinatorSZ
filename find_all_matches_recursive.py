import os
import cv2
import numpy as np
from pathlib import Path


def calculate_mse(image1, image2):
    # Приведение типов для правильного вычисления
    if image1.dtype != np.float64:
        image1 = image1.astype(np.float64)
    if image2.dtype != np.float64:
        image2 = image2.astype(np.float64)
    
    # Вычисление MSE
    mse = np.mean((image1 - image2) ** 2)
    return mse

def find_matches_in_directory(directory_path, reference_image_path, threshold=100):
    matches = []
    
    # Загрузка ссылочного изображения
    reference_img = cv2.imread(str(reference_image_path))
    if reference_img is None:
        print(f"Не удалось загрузить ссылочное изображение: {reference_image_path}")
        return matches
    
    # Рекурсивное прохождение по директории
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = Path(root) / file
                
                # Загрузка изображения
                img = cv2.imread(str(img_path))
                if img is None:
                    continue
                
                # Вычисление MSE
                mse = calculate_mse(reference_img, img)
                
                # Проверка порога
                if mse < threshold:
                    matches.append({
                        'image_path': str(img_path),
                        'mse': mse
                    })
    
    return matches


def find_all_matches_recursive(test_image_path, icons_base_path, threshold=100):
    matches = []
    
    # Рекурсивное прохождение по всем подпапкам icons
    for root, dirs, files in os.walk(icons_base_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = Path(root) / file
                
                # Загрузка изображения
                img = cv2.imread(str(img_path))
                if img is None:
                    continue
                
                # Проверка совпадения с тестовым изображением
                mse = calculate_mse(test_image_path, img)
                
                # Проверка порога
                if mse < threshold:
                    matches.append({
                        'image_path': str(img_path),
                        'mse': mse
                    })
    
    return matches


def main():
    # Путь к тестовому изображению
    test_image_path = 'test_image.png'
    
    # Путь к директории icons
    icons_path = 'data/icons'
    
    print("Начинаем поиск совпадений в структуре icons...")
    
    # Проверка существования тестового изображения
    if not os.path.exists(test_image_path):
        print(f"Тестовое изображение {test_image_path} не найдено.")
        return
    
    # Загрузка тестового изображения
    test_img = cv2.imread(test_image_path)
    if test_img is None:
        print(f"Не удалось загрузить тестовое изображение: {test_image_path}")
        return
    
    # Поиск всех совпадений
    matches = find_all_matches_recursive(test_img, icons_path)
    
    print(f"Найдено совпадений: {len(matches)}")
    
    # Вывод результатов
    for i, match in enumerate(matches):
        print(f"Совпадение {i+1}: {match['image_path']} (MSE: {match['mse']:.2f})")
        
    # Сохранение результатов в файл
    with open('matches_results.txt', 'w') as f:
        f.write("Результаты поиска совпадений:\n")
        f.write(f"Найдено совпадений: {len(matches)}\n\n")
        for i, match in enumerate(matches):
            f.write(f"Совпадение {i+1}: {match['image_path']} (MSE: {match['mse']:.2f})\n")
    
    print("Результаты сохранены в matches_results.txt")

if __name__ == "__main__":
    main()