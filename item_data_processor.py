import os
import json
from typing import Dict, List, Any

class ItemDataProcessor:
    def __init__(self, items_dir: str):
        self.items_dir = items_dir
        self.items_data = {}

    def load_items(self):
        """Загрузка данных о предметах из файлов"""
        try:
            # Проверка существования директории
            if not os.path.exists(self.items_dir):
                print(f'Директория {self.items_dir} не существует')
                return {}
            
            # Поиск всех файлов в директории
            for root, dirs, files in os.walk(self.items_dir):
                for file in files:
                    if file.endswith('.json'):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            self.items_data[file] = data
                            
            print(f'Загружено {len(self.items_data)} файлов предметов')
            return self.items_data
        except Exception as e:
            print(f'Ошибка при загрузке предметов: {e}')
            return {}

    def get_item_by_name(self, name: str) -> Dict[str, Any]:
        """Получение предмета по имени"""
        for item_name, item_data in self.items_data.items():
            if item_name.lower() == name.lower():
                return item_data
        return {}

    def get_all_items(self) -> List[Dict[str, Any]]:
        """Получение всех предметов"""
        return list(self.items_data.values())

    def get_items_count(self) -> int:
        """Получение количества предметов"""
        return len(self.items_data)

    def print_items(self):
        """Вывод информации о предметах"""
        print(f'Информация о {len(self.items_data)} предметах:')
        for item_name, item_data in self.items_data.items():
            print(f'  {item_name}:')
            for key, value in item_data.items():
                print(f'    {key}: {value}')

# Пример использования
if __name__ == '__main__':
    processor = ItemDataProcessor('sandbox/data/items')
    processor.load_items()
    processor.print_items()
