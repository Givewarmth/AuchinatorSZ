# Анализ изображений с использованием только стандартных библиотек Python

import os
import sys

# Функция для создания карты сопоставления с детализацией

def create_detailed_mapping():
    print("Создание детализированной карты сопоставления...")
    
    # Проверяем наличие директорий
    screenshots_dir = 'data/screenshots'
    icons_dir = 'data/icons/bullet'
    
    if not os.path.exists(screenshots_dir):
        print(f"Папка {screenshots_dir} не найдена")
        return None
    
    if not os.path.exists(icons_dir):
        print(f"Папка {icons_dir} не найдена")
        return None
    
    # Получаем список файлов
    screenshot_files = [f for f in os.listdir(screenshots_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    icon_files = [f for f in os.listdir(icons_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    print(f"Найдено скриншотов: {len(screenshot_files)}")
    print(f"Найдено иконок: {len(icon_files)}")
    
    # Создаем карту сопоставления
    mapping = {}
    
    # Для каждого скриншота создаем список сопоставлений
    for screenshot in screenshot_files:
        mapping[screenshot] = []
        
        # Сравниваем с каждой иконкой
        for icon in icon_files:
            # Сравниваем по длине имени файла как простой способ оценки
            name_similarity = abs(len(screenshot) - len(icon))
            
            # Сравниваем по содержанию файлов (в упрощенном виде)
            # Для демонстрации - просто считаем количество букв в имени
            screenshot_letters = sum(1 for c in screenshot.lower() if c.isalpha())
            icon_letters = sum(1 for c in icon.lower() if c.isalpha())
            
            # Вычисляем степень схожости
            letter_difference = abs(screenshot_letters - icon_letters)
            
            # Общая оценка
            total_score = name_similarity + letter_difference
            
            mapping[screenshot].append((icon, total_score))
        
        # Сортируем по степени схожости
        mapping[screenshot].sort(key=lambda x: x[1])
        
    print("Карта сопоставления создана!")
    
    # Выводим результаты
    for screenshot, matches in mapping.items():
        print(f"\n{screenshot}:")
        for i, (icon, score) in enumerate(matches[:5]):
            print(f"  {i+1}. {icon} (оценка: {score})")
    
    return mapping

# Запускаем анализ
if __name__ == "__main__":
    create_detailed_mapping()
    print("\nАнализ завершен!")
    