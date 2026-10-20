import subprocess
import sys
import os

def run_analysis():
    try:
        # Запускаем скрипт для поиска объектов
        result = subprocess.run([sys.executable, 'final_object_finder.py'], 
                            capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("Анализ завершен успешно:")
            print(result.stdout)
        else:
            print("Ошибка при выполнении анализа:")
            print(result.stderr)
            
    except Exception as e:
        print(f"Ошибка запуска анализа: {e}")
        
if __name__ == "__main__":
    run_analysis()