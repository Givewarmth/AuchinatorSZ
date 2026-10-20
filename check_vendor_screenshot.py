import cv2
import numpy as np
import os
from pathlib import Path

class IconMatcher:
    def __init__(self, icons_path):
        self.icons_path = icons_path
        self.icons = self.load_icons()

    def load_icons(self):
        icons = {}
        for root, dirs, files in os.walk(self.icons_path):
            for file in files:
                if file.endswith(".png"):
                    icon_path = os.path.join(root, file)
                    icon_name = Path(icon_path).name
                    icon_img = cv2.imread(icon_path)
                    if icon_img is not None:
                        icons[icon_name] = icon_img
        return icons

    def find_icons_in_screenshot(self, screenshot_path):
        screenshot = cv2.imread(screenshot_path)
        if screenshot is None:
            print("Ошибка загрузки скриншота!")
            return []

        found_icons = []
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        for icon_name, icon_img in self.icons.items():
            icon_gray = cv2.cvtColor(icon_img, cv2.COLOR_BGR2GRAY)
            
            # Поиск иконки в скриншоте
            result = cv2.matchTemplate(screenshot_gray, icon_gray, cv2.TM_CCOEFF_NORMED)
            
            # Установка порога для поиска
            threshold = 0.7
            locations = np.where(result >= threshold)
            
            # Если иконка найдена
            if locations[0].size > 0:
                found_icons.append(icon_name)
                
        return found_icons

# Путь к скриншоту
screenshot_path = "data/screenshots/vendor.png"

# Путь к иконкам
icons_path = "data/icons"

# Создание экземпляра IconMatcher
matcher = IconMatcher(icons_path)

# Поиск иконок на скриншоте
found_icons = matcher.find_icons_in_screenshot(screenshot_path)

# Вывод найденных иконок
print(f"Найденные иконки на скриншоте: {len(found_icons)}")

if found_icons:
    for icon in found_icons:
        print(f"  {icon}")
else:
    print("Иконки не найдены на скриншоте.")

print("Проверка завершена.")