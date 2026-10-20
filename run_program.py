import sys
import os

# Добавляем текущую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Импортируем необходимые модули
from screenshot_processor import process_screenshots
from icon_price_mapper import map_icons_to_prices
from main_program import main
from vendor_data_reader import read_vendor_data
from mapping_reader import read_mapping
from items_reader import read_items
from crafting_calculator import load_vendor_data, load_icon_mapping


def run_all():
    """Запуск всех компонентов программы"""
    print("Запуск программы...")
    
    # Загрузка данных
    vendor_data = load_vendor_data()
    icon_mapping = load_icon_mapping()
    
    print("Данные о ценах у продавца:")
    for item, price in vendor_data.items():
        print(f"  {item}: {price}")
    
    print("Сопоставление иконок:")
    for icon, price in icon_mapping.items():
        print(f"  {icon}: {price}")
    
    # Запуск основной программы
    main()
    
    print("Программа завершена.")


if __name__ == "__main__":
    run_all()
