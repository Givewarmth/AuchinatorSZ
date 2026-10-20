
"""
Работа с данными вендора и сопоставлением с ценами
"""

import os
import json
import csv
from pathlib import Path

def load_vendor_data():
    """Загрузка данных из vendor_data.txt"""
    try:
        with open('vendor_data.txt', 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
            return lines
    except FileNotFoundError:
        print("❌ Файл vendor_data.txt не найден")
        return []

def load_mapping():
    """Загрузка сопоставления иконок с ценами"""
    try:
        with open('mapping.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ Файл mapping.json не найден или поврежден")
        return {}

def load_items_data():
    """Загрузка данных о предметах из items"""
    items_path = 'sandbox/data/items'
    items_data = {}
    
    try:
        # Проверяем существование директории
        if not os.path.exists(items_path):
            print(f"❌ Директория {items_path} не найдена")
            return {}
            
        # Рекурсивный поиск файлов
        for root, dirs, files in os.walk(items_path):
            for file in files:
                if file.endswith('.json'):
                    item_path = os.path.join(root, file)
                    try:
                        with open(item_path, 'r') as f:
                            item_data = json.load(f)
                            # Имя файла без расширения как ID предмета
                            item_id = os.path.splitext(file)[0]
                            items_data[item_id] = item_data
                    except Exception as e:
                        print(f"  ❌ Ошибка при загрузке {item_path}: {e}")
                        
        print(f"  Загружено {len(items_data)} предметов")
        return items_data
    except Exception as e:
        print(f"❌ Ошибка при загрузке предметов: {e}")
        return {}

def create_vendor_mapping():
    """Создание сопоставления данных вендора"""
    vendor_lines = load_vendor_data()
    mapping = load_mapping()
    items_data = load_items_data()
    
    print("=== СОПОСТАВЛЕНИЕ ДАННЫХ ВЕНДОРА ===")
    
    # Создаем структуру для хранения информации
    vendor_info = {
        'items': [],
        'prices': {},
        'mapping': {}
    }
    
    # Обрабатываем строки данных
    for i, line in enumerate(vendor_lines):
        print(f"Обработка строки {i+1}: {line}")
        
        # Пример парсинга строки
        parts = line.split(',')
        if len(parts) >= 2:
            item_id = parts[0].strip()
            price = parts[1].strip()
            
            # Пытаемся найти информацию о предмете
            item_info = None
            if item_id in items_data:
                item_info = items_data[item_id]
            else:
                # Проверяем, есть ли такой предмет в других местах
                for item_key, item_value in items_data.items():
                    if item_key.lower() == item_id.lower():
                        item_info = item_value
                        break
            
            vendor_info['items'].append({
                'id': item_id,
                'price': price,
                'info': item_info
            })
            
            # Добавляем в mapping
            if item_id in mapping:
                vendor_info['mapping'][item_id] = mapping[item_id]
            else:
                # Попытка найти по имени
                for key, value in mapping.items():
                    if key.lower() == item_id.lower():
                        vendor_info['mapping'][item_id] = value
                        break
    
    # Сохраняем результат
    with open('vendor_mapping.json', 'w') as f:
        json.dump(vendor_info, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Сохранено {len(vendor_info['items'])} предметов")
    print(f"✅ Сохранено {len(vendor_info['mapping'])} сопоставлений")
    
    return vendor_info

def main():
    """Главная функция"""
    print("=== РАБОТА С ДАННЫМИ ВЕНДОРА ===")
    
    # Создаем сопоставление
    vendor_info = create_vendor_mapping()
    
    # Выводим информацию
    print("
=== РЕЗУЛЬТАТ ===")
    for item in vendor_info['items']:
        print(f"ID: {item['id']}, Цена: {item['price']}")
        if item['info']:
            print(f"  Название: {item['info'].get('name', 'Неизвестно')}")
    
    print("
=== ЗАВЕРШЕНИЕ ===")

if __name__ == "__main__":
    main()
