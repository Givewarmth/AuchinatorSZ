const fs = require('fs');
const path = require('path');

// Пути к директориям
const screenshotsDir = 'data/screenshots';
const iconsDir = 'data/icons/bullet';

// Чтение скриншотов
const screenshots = fs.readdirSync(screenshotsDir);

// Чтение иконок
const icons = fs.readdirSync(iconsDir);

// Функция для вычисления MSE (Mean Squared Error)
function calculateMSE(image1, image2) {
  let mse = 0;
  for (let i = 0; i < image1.length; i++) {
    mse += Math.pow(image1[i] - image2[i], 2);
  }
  return mse / image1.length;
}

// Функция для вычисления среднего значения пикселей
function calculateAveragePixel(image) {
  let sum = 0;
  for (let i = 0; i < image.length; i++) {
    sum += image[i];
  }
  return sum / image.length;
}

// Функция для сравнения пикселей
function comparePixels(pixel1, pixel2) {
  // Вычисление разности между пикселями
  return Math.abs(pixel1 - pixel2);
}

// Функция для загрузки изображений (заглушка)
function loadImage(imagePath) {
  // В реальной реализации здесь будет загрузка изображений
  // Для демонстрации, просто возвращаем массив пикселей
  return new Array(100).fill(0).map(() => Math.floor(Math.random() * 256));
}

// Функция для сравнения изображений с использованием MSE и контрастности
function compareImages(screenshotPath, iconPath) {
  // Загрузка изображений
  const screenshotImage = loadImage(screenshotPath);
  const iconImage = loadImage(iconPath);
  
  // Вычисление MSE
  const mse = calculateMSE(screenshotImage, iconImage);
  
  // Вычисление контрастности
  const averagePixel1 = calculateAveragePixel(screenshotImage);
  const averagePixel2 = calculateAveragePixel(iconImage);
  const contrast = Math.abs(averagePixel1 - averagePixel2);
  
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
    
    // Вызов функции сравнения
    const result = compareImages(screenshotFullPath, iconFullPath);
    results.push(result);
  });
});

// Вывод результатов
console.log('Результаты сравнения:');
results.forEach(result => {
  console.log(`Сравнение ${result.screenshot} с ${result.icon}: MSE = ${result.mse.toFixed(2)}, Контрастность = ${result.contrast.toFixed(2)}`);
});

console.log('Сравнение завершено.');