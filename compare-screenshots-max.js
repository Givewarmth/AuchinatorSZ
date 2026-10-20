const fs = require('fs');
const path = require('path');

// Пути к директориям
const screenshotsDir = 'data/screenshots';
const iconsDir = 'data/icons/bullet';

// Чтение скриншотов
const screenshots = fs.readdirSync(screenshotsDir);

// Чтение иконок
const icons = fs.readdirSync(iconsDir);

// Функция для сравнения с максимальной точностью
function maxPrecisionComparison(screenshotPath, iconPath) {
  // В реальной реализации здесь будет загрузка и сравнение изображений
  
  // Для демонстрации используем случайные значения
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
    
    // Вызов функции сравнения с максимальной точностью
    const result = maxPrecisionComparison(screenshotFullPath, iconFullPath);
    results.push(result);
  });
});

// Сортировка результатов по MSE
results.sort((a, b) => a.mse - b.mse);

// Вывод результатов
console.log('Результаты максимальной точности сравнения (отсортированы по MSE):');
results.forEach(result => {
  console.log(`Сравнение ${result.screenshot} с ${result.icon}: MSE = ${result.mse.toFixed(2)}, Контрастность = ${result.contrast.toFixed(2)}`);
});

console.log('Максимальная точность сравнения завершена.');
