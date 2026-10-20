
import json
import os

def load_vendor_data():
    """Загрузка данных о вендорах из vendor_data.txt"""
    try:
        with open("vendor_data.txt", "r") as f:
            lines = f.readlines()
            
        vendors = {}
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split(": ")
                if len(parts) == 2:
                    item_name = parts[0]
                    price = int(parts[1])
                    vendors[item_name] = price
        
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
        with open("mapping.json", "r") as f:
            mapping = json.load(f)
        return mapping
    except FileNotFoundError:
        print("Ошибка: Не найден файл mapping.json")
        return {}
    except Exception as e:
        print(f"Ошибка при чтении mapping.json: {e}")
        return {}

def load_items():
    """Загрузка данных о предметах из items.txt"""
    try:
        with open("items.txt", "r") as f:
            lines = f.readlines()
            
        items = {}
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split(": ")
                if len(parts) == 2:
                    item_name = parts[0]
                    item_description = parts[1]
                    items[item_name] = item_description
        
        return items
    except FileNotFoundError:
        print("Ошибка: Не найден файл items.txt")
        return {}
    except Exception as e:
        print(f"Ошибка при чтении items.txt: {e}")
        return {}

def analyze_vendor_data():
    """Анализ данных о вендорах"""
    vendors = load_vendor_data()
    mapping = load_mapping()
    items = load_items()
    
    print("Анализ данных поставщика:")
    print("-" * 30)
    
    # Определяем базовую цену для крафта
    crafting_cost = 100  # Предположим, что базовая цена крафта 100
    
    for item_name, price in vendors.items():
        # Получаем иконку из mapping
        icon = mapping.get(item_name, "Неизвестно")
        
        # Определяем, выгоднее купить или крафтить
        if price > crafting_cost:
            comparison = "крафтить"
            difference = price - crafting_cost
        elif price < crafting_cost:
            comparison = "купить"
            difference = crafting_cost - price
        else:
            comparison = "равно"
            difference = 0
            
        print(f"{item_name}: {price} (иконка: {icon})")
        if comparison != "равно":
            print(f"  Выгоднее {comparison}: {price} {'>' if price > crafting_cost else '<'} {crafting_cost}")
        else:
            print(f"  Стоимость равна {crafting_cost}")
        print()
    
    print("Программа для крафта и аукциона готова!")

if __name__ == "__main__":
    analyze_vendor_data()
