import json
import os
import re

def load_mapping():
    with open('mapping.json', 'r') as f:
        return json.load(f)

def load_vendor_data():
    with open('vendor_data.txt', 'r') as f:
        lines = f.readlines()
        vendor_data = {}
        for line in lines:
            if line.startswith('Вендор'):
                # Используем регулярные выражения для извлечения данных
                match = re.search(r'Вендор (\d+): (\S+) -> (\S+) \(цена: (\d+)\)', line)
                if match:
                    vendor_id = match.group(1)
                    icon = match.group(2)
                    item_icon = match.group(3)
                    price = int(match.group(4))
                    vendor_data[vendor_id] = {'icon': icon, 'item_icon': item_icon, 'price': price}
        return vendor_data

def find_item_name(icon_path, mapping):
    icon_filename = os.path.basename(icon_path)
    for icon, name in mapping.items():
        if icon == icon_filename:
            return name
    return 'Неизвестный предмет'

def analyze_vendor_data():
    mapping = load_mapping()
    vendor_data = load_vendor_data()
    
    print('Анализ данных вендора:')
    for vendor_id, data in vendor_data.items():
        icon = data['icon']
        item_icon = data['item_icon']
        price = data['price']
        item_name = find_item_name(item_icon, mapping)
        print(f'Вендор {vendor_id}: {icon} -> {item_name} (цена: {price})')

def main():
    analyze_vendor_data()

if __name__ == "__main__":
    main()