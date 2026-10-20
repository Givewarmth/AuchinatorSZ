import os
import glob


def load_images_from_folder(folder_path):
    # Получаем список всех файлов в папке
    files = glob.glob(os.path.join(folder_path, "*.png"))
    return files


def compare_images(img1_path, img2_path):
    # Простое сравнение по размеру файлов
    try:
        size1 = os.path.getsize(img1_path)
        size2 = os.path.getsize(img2_path)
        return abs(size1 - size2) / (size1 + size2) if (size1 + size2) > 0 else 0
    except:
        return 1.0


def main():
    # Получаем список файлов изображений
    screenshot_files = load_images_from_folder('data/screenshots')
    icon_files = load_images_from_folder('data/icons/bullet')
    
    print("Сравнение файлов:")
    
    for screenshot in screenshot_files:
        for icon in icon_files:
            similarity = compare_images(screenshot, icon)
            print(f'{os.path.basename(screenshot)} vs {os.path.basename(icon)}: {similarity:.4f}')

if __name__ == '__main__':
    main()