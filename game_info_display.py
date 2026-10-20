import sys
import os

# Добавляем текущую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Импортируем необходимые модули
from vendor_data_reader import read_vendor_data
from icon_price_mapper import map_icons_to_prices
from crafting_calculator import load_vendor_data, load_icon_mapping
from items_reader import read_items


def display_game_info():
    """Отображение информации в игре"""
    print("Отображение информации в игре...")
    
    # Загрузка данных
    vendor_data = load_vendor_data()
    icon_mapping = load_icon_mapping()
    
    print("Информация о ценах у продавца:")
    for item, price in vendor_data.items():
        print(f"  {item}: {price}")
    
    print("Сопоставление иконок:")
    for icon, price in icon_mapping.items():
        print(f"  {icon}: {price}")
    
    print("Информация в игре отображена.")


def main():
    display_game_info()

if __name__ == "__main__":
    main()
