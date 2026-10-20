import os
import sys
from pathlib import Path


def get_icon_files(icon_dir="sandbox/data/icons"):
    """Получение списка файлов иконок"""
    icon_files = []
    
    try:
        # Проверяем, существует ли директория
        if os.path.exists(icon_dir):
            for root, dirs, files in os.walk(icon_dir):
                for file in files:
                    if file.endswith(('.png', '.jpg', '.jpeg')):
                        icon_files.append(os.path.join(root, file))
        else:
            print(f"Директория иконок {icon_dir} не найдена")
            
        return icon_files
    except Exception as e:
        print(f"Ошибка при получении файлов иконок: {e}")
        return icon_files


def get_screenshot_files(screenshot_dir="sandbox/data/screenshots"):
    """Получение списка файлов скриншотов"""
    screenshot_files = []
    
    try:
        # Проверяем, существует ли директория
        if os.path.exists(screenshot_dir):
            for root, dirs, files in os.walk(screenshot_dir):
                for file in files:
                    if file.endswith(('.png', '.jpg', '.jpeg')):
                        screenshot_files.append(os.path.join(root, file))
        else:
            print(f"Директория скриншотов {screenshot_dir} не найдена")
            
        return screenshot_files
    except Exception as e:
        print(f"Ошибка при получении файлов скриншотов: {e}")
        return screenshot_files


def process_icon_files():
    """Обработка файлов иконок"""
    icon_files = get_icon_files()
    
    if not icon_files:
        print("Нет файлов иконок для обработки")
        return
    
    print(f"Найдено {len(icon_files)} файлов иконок:")
    for file in icon_files:
        print(f"  {file}")
        
    # Здесь будет логика обработки иконок
    print("Файлы иконок обработаны")


def process_screenshot_files():
    """Обработка файлов скриншотов"""
    screenshot_files = get_screenshot_files()
    
    if not screenshot_files:
        print("Нет файлов скриншотов для обработки")
        return
    
    print(f"Найдено {len(screenshot_files)} файлов скриншотов:")
    for file in screenshot_files:
        print(f"  {file}")
        
    # Здесь будет логика обработки скриншотов
    print("Файлы скриншотов обработаны")


def main():
    print("Обработка файлов иконок и скриншотов")
    
    # Обработка файлов иконок
    process_icon_files()
    
    # Обработка файлов скриншотов
    process_screenshot_files()
    
    print("Обработка файлов завершена")

if __name__ == "__main__":
    main()