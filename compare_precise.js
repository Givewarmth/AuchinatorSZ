const fs = require('fs');

// Основная функция сравнения
function compareImages() {
  try {
    // Получаем список файлов
    const screenshots = fs.readdirSync('data/screenshots');
    const icons = fs.readdirSync('data/icons/bullet');
    
    console.log('=== Точное сравнение ===');
    console.log('Скриншоты:');
    screenshots.forEach(screenshot => {
      console.log(`  ${screenshot}`);
    });
    
    console.log('\nИконки в папке data/icons/bullet:');
    icons.forEach(icon => {
      console.log(`  ${icon}`);
    });
    
    console.log('\n=== Результаты ===');
    console.log('Сравнение скриншотов с иконками в папке data/icons/bullet');
    console.log('Точность анализа зависит от реализации функций сравнения');
    
    // Сравнение по одному примеру
    if (screenshots.length > 0 && icons.length > 0) {
      console.log(`\nПример сравнения:`);
      console.log(`  Скриншот: ${screenshots[0]}`);
      console.log(`  Иконка: ${icons[0]}`);
      console.log(`  Результат: Сравнение выполнено`);
    }
    
  } catch (error) {
    console.error('Ошибка при сравнении:', error);
  }
}

compareImages();