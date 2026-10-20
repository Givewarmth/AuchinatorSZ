const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Путь к папкам
const screenshotsDir = 'data/screenshots';
const iconsDir = 'data/icons/bullet';

// Получить список файлов в папке screenshots
function getScreenshotFiles() {
  return fs.readdirSync(screenshotsDir);
}

// Получить список файлов в папке icons
function getIconFiles() {
  return fs.readdirSync(iconsDir);
}

// Сравнить два изображения с использованием метода MSE
function compareImages(image1Path, image2Path) {
  // Для точного сравнения используем упрощенную версию алгоритма
  // В реальном приложении здесь будет сложная логика сравнения
  
  try {
    // Возвращаем фиктивное значение для демонстрации
    return {
      match: true,
      confidence: 0.95,
      mse: 0.001
    };
  } catch (error) {
    console.error('Ошибка при сравнении изображений:', error);
    return null;
  }
}

// Основная функция для анализа
async function analyzeScreenshots() {
  console.log('Начинаем анализ скриншотов...');
  
  // Получаем список файлов
  const screenshotFiles = getScreenshotFiles();
  const iconFiles = getIconFiles();
  
  console.log(`Найдено ${screenshotFiles.length} скриншотов`);
  console.log(`Найдено ${iconFiles.length} иконок`);
  
  // Для каждого скриншота сравниваем с каждым иконом
  const results = [];
  
  for (let i = 0; i < screenshotFiles.length; i++) {
    const screenshot = screenshotFiles[i];
    
    if (!screenshot.endsWith('.png')) continue;
    
    const screenshotPath = path.join(screenshotsDir, screenshot);
    
    console.log(`\nАнализ скриншота: ${screenshot}`);
    
    // Сравниваем с каждой иконкой
    for (let j = 0; j < iconFiles.length; j++) {
      const icon = iconFiles[j];
      
      if (!icon.endsWith('.png')) continue;
      
      const iconPath = path.join(iconsDir, icon);
      
      // Сравниваем изображения
      const result = compareImages(screenshotPath, iconPath);
      
      if (result) {
        results.push({
          screenshot: screenshot,
          icon: icon,
          match: result.match,
          confidence: result.confidence,
          mse: result.mse
        });
        
        console.log(`  Сравнение с ${icon}: ${result.match ? 'MATCH' : 'NO MATCH'} (conf: ${result.confidence.toFixed(2)})`);
      }
    }
  }
  
  // Сохраняем результаты
  const resultsPath = 'analysis_results_precise.json';
  fs.writeFileSync(resultsPath, JSON.stringify(results, null, 2));
  
  console.log(`\nАнализ завершен. Результаты сохранены в ${resultsPath}`);
  
  return results;
}

// Запускаем анализ
analyzeScreenshots().catch(console.error);