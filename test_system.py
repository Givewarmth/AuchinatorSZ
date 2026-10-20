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


def test_all():
    """Тестирование всей системы"""
    print("Тестирование всей системы...")
    
    # Тестирование загрузки данных
    try:
        vendor_data = load_vendor_data()
        print("✓ Загрузка данных о ценах у продавца успешна")
        
        icon_mapping = load_icon_mapping()
        print("✓ Загрузка сопоставления иконок успешна")
        
        # Тестирование обработки скриншотов
        process_screenshots()
        print("✓ Обработка скриншотов успешна")
        
        # Тестирование сопоставления иконок с ценами
        map_icons_to_prices()
        print("✓ Сопоставление иконок с ценами успешна")
        
        # Тестирование основной программы
        main()
        print("✓ Основная программа успешна")
        
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        
    print("Тестирование завершено.")


if __name__ == "__main__":
    test_all()
