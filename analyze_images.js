const fs = require('fs');

// Функция для чтения и анализа данных
function analyzeImages() {
  try {
    // Чтение файлов в папках
    const screenshots = fs.readdirSync('data/screenshots');
    const icons = fs.readdirSync('data/icons/bullet');
    
    console.log('Анализ изображений:');
    console.log('Скриншоты:');
    screenshots.forEach(screenshot => {
      console.log(`  ${screenshot}`);
    });
    
    console.log('Иконки:');
    icons.forEach(icon => {
      console.log(`  ${icon}`);
    });
    
    console.log('\nДля точного сравнения необходимо:');
    console.log('- Установить библиотеки для работы с изображениями');
    console.log('- Использовать OpenCV или Pillow');
    
  } catch (error) {
    console.error('Ошибка при анализе:', error);
  }
}

analyzeImages();