import sys
import os

# Добавляем текущую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Импортируем необходимые модули
from vendor_data_reader import read_vendor_data
from icon_price_mapper import map_icons_to_prices
from crafting_calculator import load_vendor_data, load_icon_mapping
from items_reader import read_items


def generate_report():
    """Генерация отчета по сравнению цен"""
    print("Генерация отчета по сравнению цен...")
    
    # Загрузка данных
    vendor_data = load_vendor_data()
    icon_mapping = load_icon_mapping()
    
    print("Цены у продавца:")
    for item, price in vendor_data.items():
        print(f"  {item}: {price}")
    
    print("Сопоставление иконок:")
    for icon, price in icon_mapping.items():
        print(f"  {icon}: {price}")
    
    # Сравнение цен
    print("Сравнение цен:")
    
    # Здесь будет логика сравнения цен
    print("Отчет готов.")
    

def main():
    generate_report()

if __name__ == "__main__":
    main()
