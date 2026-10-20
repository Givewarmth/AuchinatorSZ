// Импорт необходимых библиотек
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

// Функция для вычисления MSE между двумя изображениями
async function calculateMSE(image1, image2) {
  // Загрузка изображений
  const img1 = await sharp(image1).raw().toBuffer();
  const img2 = await sharp(image2).raw().toBuffer();
  
  // Преобразование в массивы байтов
  const buffer1 = new Uint8Array(img1);
  const buffer2 = new Uint8Array(img2);
  
  // Вычисление MSE
  let sum = 0;
  for (let i = 0; i < buffer1.length; i++) {
    const diff = buffer1[i] - buffer2[i];
    sum += diff * diff;
  }
  
  return sum / buffer1.length;
}

// Функция для сравнения скриншота с иконками
async function compareScreenshotWithIcons(screenshotPath, iconsFolder) {
  const results = [];
  
  // Получение списка файлов иконок
  const iconFiles = fs.readdirSync(iconsFolder);
  
  // Сравнение скриншота с каждой иконкой
  for (const iconFile of iconFiles) {
    const iconPath = path.join(iconsFolder, iconFile);
    try {
      const mse = await calculateMSE(screenshotPath, iconPath);
      results.push({
        icon: iconFile,
        mse: mse
      });
    } catch (error) {
      console.log(`Ошибка при сравнении ${iconFile}: ${error}`);
    }
  }
  
  // Сортировка результатов по MSE
  results.sort((a, b) => a.mse - b.mse);
  
  return results;
}

// Основная функция
async function main() {
  // Путь к скриншоту
  const screenshotPath = 'data/screenshots/vendor.png';
  
  // Путь к папке с иконками
  const iconsFolder = 'data/icons/bullet';
  
  // Сравнение скриншота с иконками
  const results = await compareScreenshotWithIcons(screenshotPath, iconsFolder);
  
  // Вывод результатов
  console.log('Результаты сравнения:');
  results.slice(0, 10).forEach((result, index) => {
    console.log(`${index + 1}. ${result.icon} - MSE: ${result.mse}`);
  });
  
  // Создание карты сопоставления
  const mapping = {};
  results.forEach((result, index) => {
    mapping[result.icon] = index + 1;
  });
  
  console.log('Карта сопоставления:');
  Object.entries(mapping).forEach(([icon, rank]) => {
    console.log(`${icon}: ${rank}`);
  });
}

// Запуск основной функции
main();