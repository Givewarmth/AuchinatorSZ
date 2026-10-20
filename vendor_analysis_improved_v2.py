
import json
import os
from typing import Dict, List

class VendorAnalyzer:
    def __init__(self, crafting_cost: int = 100):
        self.crafting_cost = crafting_cost
        self.vendors = {}
        self.mapping = {}
        self.items = {}
    
    def load_vendor_data(self, filename: str = "vendor_data.txt") -> Dict[str, int]:
        """Загрузка данных о вендорах из файла"""
        try:
            with open(filename, "r") as f:
                lines = f.readlines()
            
            vendors = {}
            for line in lines:
                line = line.strip()
                if line:
                    parts = line.split(": ")
                    if len(parts) == 2:
                        item_name = parts[0]
                        price = int(parts[1])
                        vendors[item_name] = price
            
            self.vendors = vendors
            return vendors
        except FileNotFoundError:
            print(f"Ошибка: Не найден файл {filename}")
            return {}
        except Exception as e:
            print(f"Ошибка при чтении {filename}: {e}")
            return {}
    
    def load_mapping(self, filename: str = "mapping.json") -> Dict[str, str]:
        """Загрузка данных из mapping.json"""
        try:
            with open(filename, "r") as f:
                mapping = json.load(f)
            self.mapping = mapping
            return mapping
        except FileNotFoundError:
            print(f"Ошибка: Не найден файл {filename}")
            return {}
        except Exception as e:
            print(f"Ошибка при чтении {filename}: {e}")
            return {}
    
    def load_items(self, filename: str = "items.txt") -> Dict[str, str]:
        """Загрузка данных о предметах из items.txt"""
        try:
            with open(filename, "r") as f:
                lines = f.readlines()
            
            items = {}
            for line in lines:
                line = line.strip()
                if line:
                    parts = line.split(": ")
                    if len(parts) == 2:
                        item_name = parts[0]
                        item_description = parts[1]
                        items[item_name] = item_description
            
            self.items = items
            return items
        except FileNotFoundError:
            print(f"Ошибка: Не найден файл {filename}")
            return {}
        except Exception as e:
            print(f"Ошибка при чтении {filename}: {e}")
            return {}
    
    def analyze(self) -> None:
        """Анализ данных о вендорах"""
        print("Анализ данных поставщика:")
        print("-" * 40)
        
        if not self.vendors:
            print("Нет данных для анализа")
            return
        
        for item_name, price in self.vendors.items():
            # Получаем иконку из mapping
            icon = self.mapping.get(item_name, "Неизвестно")
            
            # Определяем, выгоднее купить или крафтить
            if price > self.crafting_cost:
                comparison = "крафтить"
                difference = price - self.crafting_cost
                action = f"Крафтить ({price} > {self.crafting_cost})"
            elif price < self.crafting_cost:
                comparison = "купить"
                difference = self.crafting_cost - price
                action = f"Купить ({price} < {self.crafting_cost})"
            else:
                comparison = "равно"
                difference = 0
                action = f"Равно ({self.crafting_cost})"
            
            print(f"{item_name}: {price} (иконка: {icon})")
            print(f"  Действие: {action}")
            
            # Добавляем информацию о выгодности
            if comparison != "равно":
                print(f"  Выгода: {abs(difference)}")
            
            # Показываем описание предмета, если есть
            description = self.items.get(item_name, "Описание отсутствует")
            print(f"  Описание: {description}")
            print()
        
        print("=" * 40)
        print("Программа для крафта и аукциона готова!")
        print(f"Базовая цена крафта: {self.crafting_cost}")
    
    def get_recommendations(self) -> Dict[str, str]:
        """Получить рекомендации по покупке/крафту"""
        recommendations = {}
        for item_name, price in self.vendors.items():
            if price > self.crafting_cost:
                recommendations[item_name] = "крафтить"
            elif price < self.crafting_cost:
                recommendations[item_name] = "купить"
            else:
                recommendations[item_name] = "равно"
        return recommendations

def main():
    # Создаем анализатор с базовой ценой крафта 100
    analyzer = VendorAnalyzer(crafting_cost=100)
    
    # Загружаем данные
    analyzer.load_vendor_data()
    analyzer.load_mapping()
    analyzer.load_items()
    
    # Проводим анализ
    analyzer.analyze()
    
    # Получаем рекомендации
    recommendations = analyzer.get_recommendations()
    print("Рекомендации:")
    for item, action in recommendations.items():
        print(f"  {item}: {action}")

if __name__ == "__main__":
    main()
