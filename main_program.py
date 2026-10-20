import os
import sys
from screenshot_processor import ScreenshotProcessor
from icon_price_mapper import IconPriceMapper

class MainProgram:
    def __init__(self):
        self.processor = ScreenshotProcessor()
        self.mapper = IconPriceMapper()
        
    def run(self):
        """Основной цикл программы"""
        print("Запуск программы для обработки скриншотов и сравнения с иконками")
        
        # Загрузка данных
        try:
            self.processor.load_icons()
            self.mapper.load_mapping()
            self.mapper.load_vendor_data()
            print("Данные загружены успешно")
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
            return
        
        # Основная логика программы
        print("Программа готова к использованию")
        
        # Пример использования
        try:
            # Проверяем наличие скриншотов
            screenshot_files = os.listdir('screenshots')
            if screenshot_files:
                print(f"Найдено {len(screenshot_files)} скриншотов")
                
                # Пример обработки первого скриншота
                first_screenshot = os.path.join('screenshots', screenshot_files[0])
                processed = self.processor.process_screenshot(first_screenshot)
                print(f"Скриншот {screenshot_files[0]} обработан")
            else:
                print("Нет скриншотов для обработки")
        except Exception as e:
            print(f"Ошибка при обработке скриншотов: {e}")
            
        print("Программа завершена")

if __name__ == "__main__":
    program = MainProgram()
    program.run()
    print("Основная программа готова")
