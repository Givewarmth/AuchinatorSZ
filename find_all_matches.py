
import cv2

import numpy as np

import os

from sklearn.metrics.pairwise import cosine_similarity


def load_images_from_paths(paths):

    images = []

    for path in paths:

        if os.path.exists(path):

            img = cv2.imread(path)

            if img is not None:

                images.append(img)

        else:

            print(f"Файл не найден: {path}")

    return images


def calculate_similarity(img1, img2):

    # Преобразуем в оттенки серого

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) if len(img1.shape) == 3 else img1

    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) if len(img2.shape) == 3 else img2

    
    # Вычисляем MSE

    mse = np.mean((gray1.astype(float) - gray2.astype(float)) ** 2)

    return mse


def find_all_matches_with_details(test_image, reference_images):

    matches = []

    for i, ref_img in enumerate(reference_images):

        try:

            mse = calculate_similarity(test_image, ref_img)

            matches.append((mse, i, ref_img.shape))

        except Exception as e:

            print(f"Ошибка при сравнении {i}: {e}")

    return sorted(matches, key=lambda x: x[0])


# Основной блок

print("Поиск всех совпадений...")


# Загружаем тестовое изображение

test_path = "test_image.png"

if os.path.exists(test_path):

    test_img = cv2.imread(test_path)

    if test_img is not None:

        print(f"Тестовое изображение загружено: {test_img.shape}")

        
        # Загружаем все reference изображения

        ref_paths = ["ref1.png", "ref2.png", "ref3.png", "ref4.png"]

        ref_images = load_images_from_paths(ref_paths)

        
        if len(ref_images) > 0:

            print(f"Найдено {len(ref_images)} ссылочных изображений")

            # Находим все совпадения

            all_matches = find_all_matches_with_details(test_img, ref_images)

            print("Все совпадения (от лучшего к худшему):")

            for i, (mse, idx, shape) in enumerate(all_matches):

                print(f"{i+1}. MSE: {mse:.2f} - Ссылка {idx+1} ({shape[0]}x{shape[1]})")

            
            # Показываем только первые 5 совпадений

            print("\nПервые 5 совпадений:")

            for i in range(min(5, len(all_matches))):

                mse, idx, shape = all_matches[i]

                print(f"{i+1}. MSE: {mse:.2f} - Ссылка {idx+1}")

        else:

            print("Нет доступных ссылочных изображений")

    else:

        print("Не удалось загрузить тестовое изображение")

else:

    print("Тестовое изображение не найдено")

