import json
import os

class VendorOptimizer:
    def __init__(self):
        self.mapping = {}
        self.load_mapping()

    def load_mapping(self):
        """Загрузка данных из mapping.json"""
        try:
            with open('mapping.json', 'r') as f:
                self.mapping = json.load(f)
        except FileNotFoundError:
            print("Файл mapping.json не найден")

    def get_vendor_price(self, vendor_icon):
        """Получение цены вендора по иконке"""
        if vendor_icon in self.mapping:
            return self.mapping[vendor_icon]
        return None

    def optimize_purchase(self, item_name, vendor_price, crafting_cost):
        """Оптимизация покупки"""
        if vendor_price < crafting_cost:
            return "Покупка"
        elif vendor_price > crafting_cost:
            return "Крафтинг"
        else:
            return "Без разницы"

    def run(self):
        """Основной метод запуска"""
        print("Оптимизатор вендоров запущен")
        
        # Пример использования
        vendors = [
            'vendor.png',
            'vendor1.png',
            'vendor2.png',
            'vendor3.png',
            'vendor4.png',
            'vendor5.png'
        ]
        
        for vendor in vendors:
            price = self.get_vendor_price(vendor)
            print(f"Вендор {vendor} -> {price}")

if __name__ == "__main__":
    optimizer = VendorOptimizer()
    optimizer.run()
