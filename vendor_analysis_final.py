import json
import os

def load_vendor_data():
    """Загружает данные о ценах от поставщика"""
    try:
        with open('vendor_data.txt', 'r') as f:
            lines = f.readlines()
            vendor_data = {}
            for line in lines:
                line = line.strip()
                if line:
                    item, price = line.split(': ')
                    vendor_data[item] = int(price)
            return vendor_data
    except FileNotFoundError:
        print("Файл vendor_data.txt не найден")
        return {}

def load_mapping():
    """Загружает mapping.json"""
    try:
        with open('mapping.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Файл mapping.json не найден")
        return {}

def analyze_vendor_data():
    """Анализирует данные и показывает выгоду между покупкой и крафтом"""
    vendor_data = load_vendor_data()
    mapping = load_mapping()
    
    if not vendor_data or not mapping:
        print("Невозможно продолжить анализ без данных")
        return
    
    print("Анализ данных поставщика:")
    print("-" * 30)
    
    # Сопоставляем иконки с ценами
    for item, price in vendor_data.items():
        icon = mapping.get(item, "неизвестно")
        print(f"{item}: {price} (иконка: {icon})")
        
        # Для демонстрации расчета выгоды
        # Предположим, что крафт стоит 100 ресурсов
        crafting_cost = 100
        if price < crafting_cost:
            print(f"  Выгоднее купить: {price} < {crafting_cost}")
        else:
            print(f"  Выгоднее крафтить: {price} >= {crafting_cost}")
        print()

def calculate_best_option():
    """Рассчитывает оптимальное решение для каждого предмета"""
    vendor_data = load_vendor_data()
    mapping = load_mapping()
    
    if not vendor_data or not mapping:
        print("Невозможно продолжить анализ без данных")
        return
    
    crafting_cost = 100  # Стоимость крафта для демонстрации
    
    print("Расчет выгоды для каждого предмета:")
    print("-" * 30)
    
    for item, price in vendor_data.items():
        icon = mapping.get(item, "неизвестно")
        
        # Рассчитываем выгоду
        if price < crafting_cost:
            difference = crafting_cost - price
            print(f"{item}: купить ({price}) выгоднее крафта ({crafting_cost}) на {difference}")
        elif price > crafting_cost:
            difference = price - crafting_cost
            print(f"{item}: крафт ({crafting_cost}) выгоднее покупки ({price}) на {difference}")
        else:
            print(f"{item}: стоимость равна ({price}) - нет выгоды")
        
        print(f"  Иконка: {icon}")
        print()

# Запускаем анализ
print("Первичный анализ:")
analyze_vendor_data()
print("\nРасчет выгоды:")
calculate_best_option()
