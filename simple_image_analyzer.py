# Простой анализ изображений
import os

# Функция для создания карты сопоставления
# Используем только стандартные библиотеки Python

def create_mapping():
    print("Создание карты сопоставления...")
    
    # Проверяем наличие директорий
    screenshots_dir = 'data/screenshots'
    icons_dir = 'data/icons/bullet'
    
    if not os.path.exists(screenshots_dir):
        print(f"Папка {screenshots_dir} не найдена")
        return
    
    if not os.path.exists(icons_dir):
        print(f"Папка {icons_dir} не найдена")
        return
    
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
            # Простая строковая оценка
            similarity = len(screenshot) - len(icon)
            mapping[screenshot].append((icon, similarity))
        
        # Сортируем по степени схожости
        mapping[screenshot].sort(key=lambda x: x[1])
        
    print("Карта сопоставления создана!")
    
    # Выводим результаты
    for screenshot, matches in mapping.items():
        print(f"{screenshot}:")
        for i, (icon, score) in enumerate(matches[:3]):
            print(f"  {i+1}. {icon} (оценка: {score})")
    
    return mapping

# Запускаем анализ
if __name__ == "__main__":
    create_mapping()