import json
import os

def load_vendor_data():
    """Загрузка данных о вендорах"""
    try:
        with open('vendor_data.json', 'r') as f:
            vendor_data = json.load(f)
        return vendor_data
    except FileNotFoundError:
        print("Ошибка: Не найден файл vendor_data.json")
        return {}
    except Exception as e:
        print(f"Ошибка при чтении vendor_data.json: {e}")
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

def load_items_data():
    """Загрузка данных о предметах"""
    try:
        with open('items_data.json', 'r') as f:
            items_data = json.load(f)
        return items_data
    except FileNotFoundError:
        print("Ошибка: Не найден файл items_data.json")
        return {}
    except Exception as e:
        print(f"Ошибка при чтении items_data.json: {e}")
        return {}

def analyze_vendor_prices():
    """Анализ цен вендоров и сопоставление с предметами"""
    vendors = load_vendor_data()
    mapping = load_mapping()
    items = load_items_data()
    
    print("=== АНАЛИЗ ЦЕН ВЕНДОРОВ ===")
    
    # Сопоставление иконок с ценами
    print("\nДанные о вендорах:")
    for vendor_id, data in vendors.items():
        print(f"  {vendor_id}: {data['icon']} -> цена: {data['price']}")
        
        # Поиск соответствия с предметами
        if data['icon'] in mapping:
            item_name = mapping[data['icon']]
            print(f"    Сопоставление с предметом: {item_name}")
            
            # Проверка цены предмета в игре
            if item_name in items:
                item_price = items[item_name]['price']
                print(f"    Цена в игре: {item_price}")
                
                # Сравнение цен
                if item_price > data['price']:
                    print(f"    Выгода: Купить у вендора ({data['price']}) выгоднее чем купить в игре ({item_price})")
                elif item_price < data['price']:
                    print(f"    Выгода: Крафтить выгоднее чем купить у вендора ({data['price']})")
                else:
                    print(f"    Цена: Стоит одинаково")
            else:
                print(f"    Предмет не найден в данных о предметах")
        else:
            print(f"    Иконка не найдена в mapping.json")
    
    print("\n=== ЗАКЛЮЧЕНИЕ ===")
    print("Программа для крафта и аукциона готова!")
    
if __name__ == "__main__":
    analyze_vendor_prices()