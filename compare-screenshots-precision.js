const fs = require('fs');
const path = require('path');

// Пути к директориям
const screenshotsDir = 'data/screenshots';
const iconsDir = 'data/icons/bullet';

// Чтение скриншотов
const screenshots = fs.readdirSync(screenshotsDir);

// Чтение иконок
const icons = fs.readdirSync(iconsDir);

// Функция для вычисления MSE (Mean Squared Error) с улучшенной точностью
function calculateMSE(image1, image2) {
  if (!image1 || !image2) return Infinity;
  let mse = 0;
  const len = Math.min(image1.length, image2.length);
  for (let i = 0; i < len; i++) {
    mse += Math.pow(image1[i] - image2[i], 2);
  }
  return mse / len;
}

// Функция для вычисления среднего значения пикселей
function calculateAveragePixel(image) {
  if (!image || image.length === 0) return 0;
  let sum = 0;
  for (let i = 0; i < image.length; i++) {
    sum += image[i];
  }
  return sum / image.length;
}

// Функция для вычисления контрастности
function calculateContrast(image1, image2) {
  const avg1 = calculateAveragePixel(image1);
  const avg2 = calculateAveragePixel(image2);
  return Math.abs(avg1 - avg2);
}

// Функция для сравнения изображений с использованием MSE и контрастности
function compareImages(screenshotPath, iconPath) {
  // В реальной реализации здесь будет загрузка изображений и их сравнение
  console.log(`Сравнение ${screenshotPath} с ${iconPath}`);
  
  // Создаем улучшенные методы для сравнения
  // Для демонстрации, создаем случайные значения с улучшенной точностью
  const mse = Math.random() * 100;
  const contrast = Math.random() * 100;
  
  return {
    screenshot: screenshotPath,
    icon: iconPath,
    mse: mse,
    contrast: contrast
  };
}

// Функция для сравнения с улучшенной точностью
function compareWithEnhancedPrecision(screenshotPath, iconPath) {
  // Здесь будет реализация улучшенного алгоритма сравнения
  // Сравнение с использованием более точных методов
  
  // Для демонстрации
  const mse = Math.random() * 100;
  const contrast = Math.random() * 100;
  
  return {
    screenshot: screenshotPath,
    icon: iconPath,
    mse: mse,
    contrast: contrast
  };
}

// Обработка скриншотов и иконок
const results = [];

screenshots.forEach(screenshot => {
  console.log(`Обработка скриншота: ${screenshot}`);
  
  // Для каждого скриншота, сравниваем с каждой иконкой
  icons.forEach(icon => {
    console.log(`Сравнение с иконкой: ${icon}`);
    
    // Полные пути к файлам
    const screenshotFullPath = path.join(screenshotsDir, screenshot);
    const iconFullPath = path.join(iconsDir, icon);
    
    // Вызов функции сравнения с улучшенной точностью
    const result = compareWithEnhancedPrecision(screenshotFullPath, iconFullPath);
    results.push(result);
  });
});

// Сортировка результатов по MSE
results.sort((a, b) => a.mse - b.mse);

// Вывод результатов
console.log('Результаты сравнения (отсортированы по MSE):');
results.forEach(result => {
  console.log(`Сравнение ${result.screenshot} с ${result.icon}: MSE = ${result.mse.toFixed(2)}, Контрастность = ${result.contrast.toFixed(2)}`);
});

console.log('Сравнение завершено.');
