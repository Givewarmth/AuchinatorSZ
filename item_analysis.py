import json
from collections import Counter

# Загружаем данные из mapping_report.json
with open('mapping_report.json', 'r') as f:
    data = json.load(f)

# Получаем список всех предметов
items = data['mapping_details']['valid_items']

# Подсчитываем количество предметов
print(f"Общее количество предметов в списке: {len(items)}")

# Подсчитываем уникальные предметы по имени
item_names = [item['name'] for item in items]
item_counts = Counter(item_names)
unique_items = len(item_counts)
print(f"Количество уникальных предметов: {unique_items}")

# Выводим дублирующиеся предметы
duplicated_items = [item for item, count in item_counts.items() if count > 1]
if duplicated_items:
    print("Дублирующиеся предметы:")
    for item in duplicated_items:
        print(f"  {item}: {item_counts[item]} раз")
else:
    print("Нет дублирующихся предметов")

# Выводим количество дублированных предметов
print(f"Количество дублированных предметов: {len(duplicated_items)}")

# Проверяем общую информацию
print(f"Всего предметов: {data['mapping_details']['total_matches']}")
print(f"Дублирующихся ID: {len(data['mapping_details']['duplicate_ids'])}")

# Проверяем уникальные имена предметов
unique_names = list(item_counts.keys())
print(f"Первые 10 уникальных имен:")
for i, name in enumerate(unique_names[:10]):
    print(f"  {i+1}: {name}")

# Проверяем структуру отдельных предметов
print(f"\nСтруктура первого предмета:")
print(f"  ID: {items[0]['id']}")
print(f"  Name: {items[0]['name']}")
print(f"  Path: {items[0]['path']}")
print(f"  Valid: {items[0]['valid']}")n