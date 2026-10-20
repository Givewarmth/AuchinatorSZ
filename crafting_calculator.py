import json
import os
from typing import Dict, List, Tuple


class CraftingCalculator:
    """Класс для расчета выгодности крафта и покупки"""
    
    def __init__(self, vendor_data_file: str = "vendor_data.txt", mapping_file: str = "mapping.json"):
        self.vendor_data_file = vendor_data_file
        self.mapping_file = mapping_file
        self.vendor_prices = {}
        self.icon_mapping = {}
        
    def load_vendor_data(self) -> Dict:
        """Загрузка данных о ценах у продавца"""
        try:
            if os.path.exists(self.vendor_data_file):
                with open(self.vendor_data_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.strip()
                        if line:
                            parts = line.split()
                            if len(parts) >= 2:
                                item_name = parts[0]
                                price = float(parts[1])
                                self.vendor_prices[item_name] = price
            else:
                print(f"Файл {self.vendor_data_file} не найден")
                return {}
        except Exception as e:
            print(f"Ошибка загрузки данных продавца: {e}")
            return {}
        
        return self.vendor_prices
    
    def load_icon_mapping(self) -> Dict:
        """Загрузка сопоставления иконок с ценами"""
        try:
            if os.path.exists(self.mapping_file):
                with open(self.mapping_file, 'r', encoding='utf-8') as f:
                    self.icon_mapping = json.load(f)
            else:
                print(f"Файл {self.mapping_file} не найден")
                return {}
        except Exception as e:
            print(f"Ошибка загрузки сопоставления: {e}")
            return {}
        
        return self.icon_mapping
    
    def calculate_profit(self, item_name: str, crafting_cost: float) -> Tuple[float, str]:
        """Расчет выгодности покупки vs крафта"""
        vendor_price = self.vendor_prices.get(item_name, 0)
        
        if vendor_price > 0 and crafting_cost > 0:
            profit = vendor_price - crafting_cost
            if profit > 0:
                return profit, "buy"
            elif profit < 0:
                return abs(profit), "craft"
            else:
                return 0, "equal"
        else:
            return 0, "unknown"
    
    def get_best_option(self, item_name: str, crafting_cost: float) -> str:
        """Получение лучшего варианта (buy/craft/equal)"""
        profit, option = self.calculate_profit(item_name, crafting_cost)
        return option
    
    def get_profit_details(self, item_name: str, crafting_cost: float) -> Dict:
        """Получение деталей выгодности"""
        profit, option = self.calculate_profit(item_name, crafting_cost)
        return {
            "item": item_name,
            "vendor_price": self.vendor_prices.get(item_name, 0),
            "crafting_cost": crafting_cost,
            "profit": profit,
            "option": option
        }


def load_vendor_data() -> Dict:
    """Загрузка данных о ценах у продавца"""
    calc = CraftingCalculator()
    return calc.load_vendor_data()


def load_icon_mapping() -> Dict:
    """Загрузка сопоставления иконок с ценами"""
    calc = CraftingCalculator()
    return calc.load_icon_mapping()


def calculate_profit(item_name: str, crafting_cost: float) -> Tuple[float, str]:
    """Расчет выгодности покупки vs крафта"""
    calc = CraftingCalculator()
    return calc.calculate_profit(item_name, crafting_cost)


def get_best_option(item_name: str, crafting_cost: float) -> str:
    """Получение лучшего варианта (buy/craft/equal)"""
    calc = CraftingCalculator()
    return calc.get_best_option(item_name, crafting_cost)


def get_profit_details(item_name: str, crafting_cost: float) -> Dict:
    """Получение деталей выгодности"""
    calc = CraftingCalculator()
    return calc.get_profit_details(item_name, crafting_cost)


if __name__ == "__main__":
    # Пример использования
    calc = CraftingCalculator()
    vendor_data = calc.load_vendor_data()
    print("Цены у продавца:")
    for item, price in vendor_data.items():
        print(f"  {item}: {price}")
    
    # Пример расчета выгодности
    item_name = "Iron"  # Пример предмета
    crafting_cost = 100  # Пример стоимости крафта
    profit, option = calc.calculate_profit(item_name, crafting_cost)
    print(f"Выгодность для {item_name}: {profit} ({option})")
    
    details = calc.get_profit_details(item_name, crafting_cost)
    print("Детали:")
    for key, value in details.items():
        print(f"  {key}: {value}")
