
import os
import json

def check_structure():
    """Проверяет структуру данных"""
    print("=== Проверка структуры данных ===")
    
    # Проверяем существование директорий
    screenshots_dir = "sandbox/data/screenshots"
    items_dir = "sandbox/data/items"
    
    print(f"Проверяем директорию скриншотов: {screenshots_dir}")
    if os.path.exists(screenshots_dir):
        screenshots = [f for f in os.listdir(screenshots_dir) if os.path.isfile(os.path.join(screenshots_dir, f))]
        print(f"  Найдено файлов: {len(screenshots)}")
        for f in screenshots:
            print(f"    - {f}")
    else:
        print("  Директория не существует")
    
    print(f"Проверяем директорию иконок: {items_dir}")
    if os.path.exists(items_dir):
        items = [f for f in os.listdir(items_dir) if os.path.isfile(os.path.join(items_dir, f))]
        print(f"  Найдено файлов: {len(items)}")
        for f in items:
            print(f"    - {f}")
    else:
        print("  Директория не существует")
    
    # Проверяем наличие mapping.json
    mapping_file = "mapping.json"
    if os.path.exists(mapping_file):
        print(f"Файл {mapping_file} существует")
        try:
            with open(mapping_file, 'r') as f:
                data = json.load(f)
                print("  Структура mapping.json:")
                for key, value in data.items():
                    print(f"    {key}: {value}")
        except Exception as e:
            print(f"  Ошибка чтения: {e}")
    else:
        print(f"Файл {mapping_file} не существует")

def main():
    """Главная функция"""
    check_structure()

if __name__ == "__main__":
    main()
