
"""
Работа с ценами и системой крафта для вендора
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

def load_vendor_items():
    """Загрузка предметов вендора"""
    vendor_lines = load_vendor_data()
    items_data = load_items_data()
    mapping = load_mapping()
    
    vendor_items = {}
    
    for i, line in enumerate(vendor_lines):
        parts = line.split(',')
        if len(parts) >= 2:
            item_id = parts[0].strip()
            price = parts[1].strip()
            
            # Ищем информацию о предмете
            item_info = None
            if item_id in items_data:
                item_info = items_data[item_id]
            else:
                # Проверяем по имени
                for key, value in items_data.items():
                    if key.lower() == item_id.lower():
                        item_info = value
                        break
            
            vendor_items[item_id] = {
                'id': item_id,
                'price': price,
                'info': item_info,
                'name': item_info.get('name', item_id) if item_info else item_id
            }
    
    return vendor_items

def calculate_crafting_costs():
    """Расчет стоимости крафта"""
    # Загрузка данных
    vendor_items = load_vendor_items()
    
    print("=== РАСЧЕТ СТОИМОСТИ КРАФТА ===")
    
    # Пример расчета для одного предмета
    crafting_costs = {}
    
    for item_id, item_data in vendor_items.items():
        # В реальной системе здесь будет сложный алгоритм расчета
        price = item_data['price']
        
        # Пример: стоимость крафта = 1.5 * цена продажи
        crafting_costs[item_id] = {
            'item_id': item_id,
            'vendor_price': price,
            'crafting_cost': float(price) * 1.5,
            'profit_margin': float(price) * 0.2  # 20% маржа
        }
        
        print(f"{item_data['name']}:")
        print(f"  Цена у вендора: {price}")
        print(f"  Стоимость крафта: {crafting_costs[item_id]['crafting_cost']:.2f}")
        print(f"  Прибыль: {crafting_costs[item_id]['profit_margin']:.2f}")
        print()
    
    return crafting_costs

def create_auction_system():
    """Создание системы аукциона"""
    vendor_items = load_vendor_items()
    
    print("=== СИСТЕМА АУКЦИОНА ===")
    
    # Структура для аукциона
    auction_data = {
        'items': [],
        'current_time': '2026-10-16',
        'auction_status': 'active'
    }
    
    for item_id, item_data in vendor_items.items():
        auction_item = {
            'id': item_id,
            'name': item_data['name'],
            'vendor_price': item_data['price'],
            'auction_price': float(item_data['price']) * 1.1,  # 10% выше цены вендора
            'quantity': 1,
            'status': 'available',
            'bid_history': []
        }
        
        auction_data['items'].append(auction_item)
    
    # Сохраняем данные аукциона
    with open('auction_data.json', 'w') as f:
        json.dump(auction_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Создано {len(auction_data['items'])} предметов для аукциона")
    
    return auction_data

def main():
    """Главная функция"""
    print("=== РАБОТА С ЦЕНАМИ И КРАФТОМ ===")
    
    # Расчет стоимости крафта
    crafting_costs = calculate_crafting_costs()
    
    # Создание системы аукциона
    auction_data = create_auction_system()
    
    print("
=== ЗАВЕРШЕНИЕ ===")
    print("Работа с ценами и крафтом завершена.")

if __name__ == "__main__":
    main()
