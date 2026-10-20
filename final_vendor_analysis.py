
import json
import os
from typing import Dict

def load_vendor_data(filename: str = "vendor_data.txt") -> Dict[str, int]:
    """Загрузка данных о вендорах из файла"""
    try:
        with open(filename, "r") as f:
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
        print(f"Ошибка: Не найден файл {filename}")
        return {}
    except Exception as e:
        print(f"Ошибка при чтении {filename}: {e}")
        return {}

def load_mapping(filename: str = "mapping.json") -> Dict[str, str]:
    """Загрузка данных из mapping.json"""
    try:
        with open(filename, "r") as f:
            mapping = json.load(f)
        return mapping
    except FileNotFoundError:
        print(f"Ошибка: Не найден файл {filename}")
        return {}
    except Exception as e:
        print(f"Ошибка при чтении {filename}: {e}")
        return {}

def load_items(filename: str = "items.txt") -> Dict[str, str]:
    """Загрузка данных о предметах из items.txt"""
    try:
        with open(filename, "r") as f:
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
        print(f"Ошибка: Не найден файл {filename}")
        return {}
    except Exception as e:
        print(f"Ошибка при чтении {filename}: {e}")
        return {}

def analyze_vendor_data(crafting_cost: int = 100) -> None:
    """Анализ данных о вендорах"""
    vendors = load_vendor_data()
    mapping = load_mapping()
    items = load_items()
    
    print("Анализ данных поставщика:")
    print("-" * 40)
    
    if not vendors:
        print("Нет данных для анализа")
        return
    
    for item_name, price in vendors.items():
        # Получаем иконку из mapping
        icon = mapping.get(item_name, "Неизвестно")
        
        # Определяем, выгоднее купить или крафтить
        if price > crafting_cost:
            comparison = "крафтить"
            difference = price - crafting_cost
            action = f"Крафтить ({price} > {crafting_cost})"
        elif price < crafting_cost:
            comparison = "купить"
            difference = crafting_cost - price
            action = f"Купить ({price} < {crafting_cost})"
        else:
            comparison = "равно"
            difference = 0
            action = f"Равно ({crafting_cost})"
        
        print(f"{item_name}: {price} (иконка: {icon})")
        print(f"  Действие: {action}")
        
        # Добавляем информацию о выгодности
        if comparison != "равно":
            print(f"  Выгода: {abs(difference)}")
        
        # Показываем описание предмета, если есть
        description = items.get(item_name, "Описание отсутствует")
        print(f"  Описание: {description}")
        print()
    
    print("=" * 40)
    print("Программа для крафта и аукциона готова!")
    print(f"Базовая цена крафта: {crafting_cost}")

def main():
    analyze_vendor_data(crafting_cost=100)

if __name__ == "__main__":
    main()
