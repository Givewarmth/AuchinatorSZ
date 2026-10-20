import json
import os
from typing import Dict, List


class VendorDataReader:
    """Класс для чтения данных из vendor_data.txt"""
    
    def __init__(self, file_path: str = "vendor_data.txt"):
        self.file_path = file_path
        self.prices = {}
        
    def read_prices(self) -> Dict[str, float]:
        """Чтение цен из файла"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split()
                        if len(parts) >= 2:
                            item_name = parts[0]
                            price = float(parts[1])
                            self.prices[item_name] = price
            return self.prices
        except FileNotFoundError:
            print(f"Файл {self.file_path} не найден")
            return {}
        except Exception as e:
            print(f"Ошибка чтения файла: {e}")
            return {}
    
    def get_price(self, item_name: str) -> float:
        """Получение цены для конкретного предмета"""
        return self.prices.get(item_name, 0.0)
    
    def get_all_prices(self) -> Dict[str, float]:
        """Получение всех цен"""
        return self.prices


def load_vendor_data() -> Dict[str, float]:
    """Загрузка данных из vendor_data.txt"""
    reader = VendorDataReader()
    return reader.read_prices()


def get_vendor_price(item_name: str) -> float:
    """Получение цены из vendor_data.txt"""
    reader = VendorDataReader()
    return reader.get_price(item_name)


def get_all_vendor_prices() -> Dict[str, float]:
    """Получение всех цен из vendor_data.txt"""
    reader = VendorDataReader()
    return reader.get_all_prices()


if __name__ == "__main__":
    prices = load_vendor_data()
    print("Цены из vendor_data.txt:")
    for item, price in prices.items():
        print(f"  {item}: {price}")
