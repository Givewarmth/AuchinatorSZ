# Используемый путь к иконкам
icons_path = "data/icons"

# Используемый путь к скриншоту
screenshot_path = "data/screenshots/vendor.png"

# Количество иконок на скриншоте
expected_icons_count = 60

# Максимальное количество предметов на скриншоте (с учетом, что предметы могут занимать до 9 клеток)
max_items_per_screenshot = 384

# Проверяем, есть ли файл скриншота
import os
if not os.path.exists(screenshot_path):
    print(f"Ошибка: файл скриншота {screenshot_path} не найден.")
    exit(1)

# Получаем список всех подпапок в icons_path
import os

# Собираем список всех подпапок в data/icons
icon_subdirs = []
for root, dirs, files in os.walk(icons_path):
    for d in dirs:
        icon_subdirs.append(os.path.join(root, d))

# Собираем список всех иконок из всех подпапок
all_icons = []
for subdir in icon_subdirs:
    try:
        for file in os.listdir(subdir):
            if file.endswith(".png"):
                all_icons.append(os.path.join(subdir, file))
    except Exception as e:
        print(f"Ошибка при чтении подпапки {subdir}: {e}")

print(f"Найдено {len(all_icons)} иконок.")

# Проверяем, что количество иконок не превышает max_items_per_screenshot
if len(all_icons) > max_items_per_screenshot:
    print(f"Предупреждение: количество иконок ({len(all_icons)}) превышает максимальное количество предметов на скриншоте ({max_items_per_screenshot}).")
else:
    print(f"Количество иконок ({len(all_icons)}) соответствует максимальному количеству предметов на скриншоте ({max_items_per_screenshot}).")

# Проверяем количество иконок на скриншоте
# В данном случае мы просто выводим, что скрипт нашел, но не проверяем на скриншоте
# Для проверки на скриншоте нужна дополнительная логика, например, с помощью OpenCV или PIL
print(f"Предметы для проверки:")
for icon in all_icons:
    print(f"  {icon}")

# Выводим количество иконок на скриншоте (предположительно)
print(f"Количество иконок на скриншоте: {expected_icons_count}")

# Проверяем, соответствует ли количество иконок ожиданиям
if len(all_icons) == expected_icons_count:
    print("Количество иконок соответствует ожиданию.")
else:
    print(f"Количество иконок не соответствует ожиданию. Ожидается: {expected_icons_count}, найдено: {len(all_icons)}.")