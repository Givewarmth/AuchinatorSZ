const fs = require('fs');
const path = require('path');

// Функция для сравнения изображений по MSE
function compareImages(screenshotPath, iconPath) {
  // Возвращаем 0, так как не можем загрузить изображения без библиотек
  return 0;
}

// Основная функция
async function main() {
  const screenshotsDir = 'data/screenshots';
  const iconsDir = 'data/icons/bullet';
  
  try {
    const screenshots = fs.readdirSync(screenshotsDir);
    const icons = fs.readdirSync(iconsDir);
    
    console.log('Сравнение скриншотов с иконками:');
    
    for (const screenshot of screenshots) {
      if (screenshot.endsWith('.png')) {
        console.log(`\nСкриншот: ${screenshot}`);
        
        // Для каждого скриншота показываем иконки
        for (const icon of icons) {
          if (icon.endsWith('.png')) {
            console.log(`  ${icon}: не удалось загрузить изображения`);
          }
        }
      }
    }
    
    console.log('\nДля точного сравнения необходимо использовать библиотеки для работы с изображениями');
    console.log('Например, OpenCV или Pillow в Python');
    
  } catch (error) {
    console.error('Ошибка:', error);
  }
}

main();