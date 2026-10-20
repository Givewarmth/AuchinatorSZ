import json
import os
from PIL import Image
import cv2
import numpy as np

class IconPriceMapper:
    def __init__(self, mapping_file='mapping.json', vendor_data_file='vendor_data.txt'):
        self.mapping = {}
        self.vendor_data = {}
        self.mapping_file = mapping_file
        self.vendor_data_file = vendor_data_file
        
    def load_mapping(self):
        """Загрузка сопоставления иконок с ценами"""
        try:
            with open(self.mapping_file, 'r') as f:
                self.mapping = json.load(f)
        except FileNotFoundError:
            print(f"Файл {self.mapping_file} не найден")
            
    def load_vendor_data(self):
        """Загрузка данных о ценах vendors"""
        try:
            with open(self.vendor_data_file, 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if line.strip():
                        # Предполагаем, что каждая строка - это цена для предмета
                        self.vendor_data[f"item_{i}"] = line.strip()
        except FileNotFoundError:
            print(f"Файл {self.vendor_data_file} не найден")
            
    def map_icon_to_price(self, icon_name):
        """Сопоставление иконки с ценой"""
        if icon_name in self.mapping:
            return self.mapping[icon_name]
        return None
    
    def get_item_price(self, item_name):
        """Получение цены для предмета"""
        if item_name in self.vendor_data:
            return self.vendor_data[item_name]
        return None
    
    def compare_prices(self, item_name):
        """Сравнение цен для определения выгодности"""
        # Здесь будет логика сравнения цен
        pass

if __name__ == "__main__":
    mapper = IconPriceMapper()
    mapper.load_mapping()
    mapper.load_vendor_data()
    print("Сопоставление иконок с ценами готово")
    
    # Пример использования
    try:
        price = mapper.get_item_price('item_0')
        print(f"Цена для item_0: {price}")
    except Exception as e:
        print(f"Ошибка: {e}")
    
    print("Скрипт для сопоставления иконок с ценами готов")
