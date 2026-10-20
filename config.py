import os

# Конфигурация путей
CONFIG = {
    'screenshots_dir': 'sandbox/data/screenshots',
    'icons_dir': 'sandbox/data/icons',
    'items_dir': 'sandbox/data/items',
    'vendor_data_file': 'vendor_data.txt',
    'mapping_file': 'mapping.json',
    'output_dir': 'output'
}

# Проверка существования директорий
def check_directories():
    for key, path in CONFIG.items():
        if key.endswith('_dir') and key != 'output_dir':
            if not os.path.exists(path):
                print(f'Предупреждение: Директория {path} не существует')

# Инициализация конфигурации
check_directories()

# Функция для получения пути к файлу
def get_path(key):
    return CONFIG.get(key)

# Функция для получения всех путей
def get_all_paths():
    return CONFIG

# Функция для установки нового пути
def set_path(key, new_path):
    CONFIG[key] = new_path

# Функция для вывода конфигурации
def print_config():
    print('Конфигурация системы:')
    for key, path in CONFIG.items():
        print(f'  {key}: {path}')

# Проверка и создание директорий
if not os.path.exists(CONFIG['output_dir']):
    os.makedirs(CONFIG['output_dir'])
    print(f'Создана директория {CONFIG["output_dir"]}')

# Добавление в переменные окружения
os.environ['SCREENSHOTS_DIR'] = CONFIG['screenshots_dir']
os.environ['ICONS_DIR'] = CONFIG['icons_dir']

print('Конфигурация инициализирована')