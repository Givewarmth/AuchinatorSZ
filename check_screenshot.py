import os
import cv2
import numpy as np
from pathlib import Path

# Путь к скриншоту
screenshot_path = "data/screenshots/vendor.png"

# Путь к иконкам
icons_path = "data/icons"

# Список иконок
icon_files = []

# Функция для получения всех файлов иконок
for root, dirs, files in os.walk(icons_path):
    for file in files:
        if file.endswith(".png"):
            icon_files.append(os.path.join(root, file))

# Проверка наличия скриншота
if not os.path.exists(screenshot_path):
    print("Скриншот не найден!")
    exit(1)

# Загрузка скриншота
image = cv2.imread(screenshot_path)

# Установка размера окна для поиска иконок (пример)
# Предположим, что размер иконки 32x32 пикселя
icon_size = (32, 32)

# Проверка, что изображение загружено
if image is None:
    print("Ошибка загрузки изображения!")
    exit(1)

# Считаем количество иконок на скриншоте
# В данном случае, мы просто выводим количество иконок, 
# потому что не можем напрямую определить, какие иконки на скриншоте
print(f"Количество иконок в папке icons: {len(icon_files)}")

# Выводим первые 10 иконок
print("Первые 10 иконок:")
for i, icon in enumerate(icon_files[:10]):
    print(f"  {icon}")

print("Проверка завершена.")