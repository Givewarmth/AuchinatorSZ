
import json
import os

def load_vendor_data():
    """Загрузка данных о вендорах"""
    try:
        with open('vendor_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Ошибка: Не найден файл vendor_data.json")
        return {}
    except json.JSONDecodeError:
        print("Ошибка: Неверный формат JSON в файле vendor_data.json")
        return {}

def calculate_profitability():
    """Расчет выгодности крафта/покупки"""
    vendor_data = load_vendor_data()
    
    print("Данные о вендорах и ценах:")
    for item_name, data in vendor_data.items():
        print(f"  {item_name}: {data['icon']} -> цена: {data['price']}")
    
    return vendor_data

def main():
    """Основная функция программы"""
    print("Программа для крафта и аукциона")
    print("=" * 30)
    
    vendor_data = calculate_profitability()
    
    if vendor_data:
        print("\n\nРасчет выгодности:")
        for item_name, data in vendor_data.items():
            print(f"  {item_name}: {data['icon']} -> цена: {data['price']}")
    
    print("\nПрограмма готова для использования!")

if __name__ == "__main__":
    main()
