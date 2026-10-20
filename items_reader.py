import os
import json
from typing import Dict, List


class ItemsReader:
    """Класс для чтения данных из sandbox/data/items"""
    
    def __init__(self, base_path: str = "sandbox/data/items"):
        self.base_path = base_path
        self.items_data = {}
        
    def read_items(self) -> Dict[str, Dict]:
        """Чтение данных о предметах из папки items"""
        try:
            # Проверяем существование директории
            if not os.path.exists(self.base_path):
                print(f"Директория {self.base_path} не существует")
                return {}
            
            # Проходим по всем подпапкам
            for root, dirs, files in os.walk(self.base_path):
                for file in files:
                    if file.endswith(".json"):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                item_name = os.path.basename(file).replace(".json", "")
                                self.items_data[item_name] = data
                        except Exception as e:
                            print(f"Ошибка чтения файла {file_path}: {e}")
            return self.items_data
        except Exception as e:
            print(f"Ошибка чтения данных: {e}")
            return {}
    
    def get_item_data(self, item_name: str) -> Dict:
        """Получение данных для конкретного предмета"""
        return self.items_data.get(item_name, {})
    
    def get_all_items(self) -> Dict[str, Dict]:
        """Получение всех предметов"""
        return self.items_data
    
    def get_item_names(self) -> List[str]:
        """Получение списка названий предметов"""
        return list(self.items_data.keys())


def load_items_data() -> Dict[str, Dict]:
    """Загрузка данных о предметах из sandbox/data/items"""
    reader = ItemsReader()
    return reader.read_items()


def get_item_data(item_name: str) -> Dict:
    """Получение данных для предмета"""
    reader = ItemsReader()
    return reader.get_item_data(item_name)


def get_all_items() -> Dict[str, Dict]:
    """Получение всех предметов"""
    reader = ItemsReader()
    return reader.get_all_items()


def get_item_names() -> List[str]:
    """Получение списка названий предметов"""
    reader = ItemsReader()
    return reader.get_item_names()


if __name__ == "__main__":
    items = load_items_data()
    print("Данные о предметах из sandbox/data/items:")
    for item, data in items.items():
        print(f"  {item}: {data}")
