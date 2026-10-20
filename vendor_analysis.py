import json
import os

def load_vendor_data():
    """Загрузка данных о вендорах из vendor_data.txt"""
    try:
        with open('vendor_data.txt', 'r') as f:
            lines = f.readlines()
            
        vendors = {}
        for i, line in enumerate(lines):
            if line.startswith('Вендор '):
                parts = line.split(': ')
                vendor_id = parts[0].replace('Вендор ', '')
                icon_and_price = parts[1].strip()
                
                # Извлекаем информацию о иконке и цене
                icon_start = icon_and_price.find('-> ') + 3
                icon_end = icon_and_price.find(' (цена:')
                icon = icon_and_price[icon_start:icon_end]
                
                price_start = icon_and_price.find('(цена: ') + 6
                price_end = icon_and_price.find(')')
                price = int(icon_and_price[price_start:price_end])
                
                vendors[vendor_id] = {
                    'icon': icon,
                    'price': price
                }
        
        return vendors
    except FileNotFoundError:
        print("Ошибка: Не найден файл vendor_data.txt")
        return {}
    except Exception as e:
        print(f"Ошибка при чтении vendor_data.txt: {e}")
        return {}

def load_mapping():
    """Загрузка данных из mapping.json"""
    try:
        with open('mapping.json', 'r') as f:
            mapping = json.load(f)
        return mapping
    except FileNotFoundError:
        print("Ошибка: Не найден файл mapping.json")
        return {}
    except Exception as e:
        print(f"Ошибка при чтении mapping.json: {e}")
        return {}

def analyze_vendor_data():
    """Анализ данных о вендорах"""
    vendors = load_vendor_data()
    mapping = load_mapping()
    
    print("Данные о вендорах:")
    for vendor_id, data in vendors.items():
        print(f"Вендор {vendor_id}: {data['icon']} -> цена: {data['price']}")
        
    print("\nСопоставление с данными из mapping.json:")
    for vendor_id, data in vendors.items():
        if data['icon'] in mapping:
            item_name = mapping[data['icon']]
            print(f"  {data['icon']} -> {item_name}")
        else:
            print(f"  {data['icon']} -> не найдено в mapping.json")
    
    print("\nПрограмма для крафта и аукциона готова!")

if __name__ == "__main__":
    analyze_vendor_data()