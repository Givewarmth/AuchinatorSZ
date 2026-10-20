import json
import os

# Создание файла с данными о вендорах
vendor_data = {
    "Вендор 1": {
        "icon": "0o01.png",
        "price": 100
    },
    "Вендор 2": {
        "icon": "0o9d.png",
        "price": 150
    },
    "Вендор 3": {
        "icon": "0ojd.png",
        "price": 200
    },
    "Вендор 4": {
        "icon": "0omd.png",
        "price": 120
    },
    "Вендор 5": {
        "icon": "0or1.png",
        "price": 180
    },
    "Вендор 6": {
        "icon": "0rlzr.png",
        "price": 140
    }
}

# Сохранение данных в JSON файл
with open("vendor_data.json", "w") as f:
    json.dump(vendor_data, f, indent=2)

print("Файл vendor_data.json успешно создан")

# Проверка содержимого файла
with open("vendor_data.json", "r") as f:
    data = json.load(f)
    print("Содержимое vendor_data.json:")
    for vendor, info in data.items():
        print(f"  {vendor}: {info}")