const fs = require('fs');
const path = require('path');

// Функция для расчета улучшенного MSE с учетом цветовой чувствительности
function calculateEnhancedMSE(pixelDataA, pixelDataB) {
    let totalDiff = 0;
    let count = 0;
    
    // Вычисляем MSE с учетом цветовой чувствительности
    for (let i = 0; i < pixelDataA.length; i += 4) {
        const rA = pixelDataA[i];
        const gA = pixelDataA[i + 1];
        const bA = pixelDataA[i + 2];
        
        const rB = pixelDataB[i];
        const gB = pixelDataB[i + 1];
        const bB = pixelDataB[i + 2];
        
        // Используем веса для цветовой чувствительности (взвешенный MSE)
        const diff = Math.sqrt(Math.pow(rA - rB, 2) + Math.pow(gA - gB, 2) + Math.pow(bA - bB, 2));
        
        totalDiff += diff;
        count++;
    }
    
    return count > 0 ? totalDiff / count : 0;
}

// Функция для вычисления средней контрастности
function calculateContrast(pixelData) {
    let total = 0;
    let count = 0;
    
    for (let i = 0; i < pixelData.length; i += 4) {
        const r = pixelData[i];
        const g = pixelData[i + 1];
        const b = pixelData[i + 2];
        
        // Вычисляем яркость с учетом цветовой чувствительности
        const brightness = 0.299 * r + 0.587 * g + 0.114 * b;
        
        total += brightness;
        count++;
    }
    
    return count > 0 ? total / count : 0;
}

// Функция для сравнения с учетом формы и обводки
function calculateShapeSimilarity(pixelDataA, pixelDataB) {
    let matchingPixels = 0;
    let totalPixels = 0;
    
    // Сравниваем пиксели с учетом цвета и контраста
    for (let i = 0; i < pixelDataA.length; i += 4) {
        const rA = pixelDataA[i];
        const gA = pixelDataA[i + 1];
        const bA = pixelDataA[i + 2];
        
        const rB = pixelDataB[i];
        const gB = pixelDataB[i + 1];
        const bB = pixelDataB[i + 2];
        
        // Проверяем, являются ли пикселя похожими
        const colorSimilarity = Math.abs(rA - rB) < 30 && Math.abs(gA - gB) < 30 && Math.abs(bA - bB) < 30;
        
        if (colorSimilarity) {
            matchingPixels++;
        }
        totalPixels++;
    }
    
    return totalPixels > 0 ? matchingPixels / totalPixels : 0;
}

// Функция для расчета коэффициента схожести
function calculateSimilarityScore(pixelDataA, pixelDataB) {
    const mse = calculateEnhancedMSE(pixelDataA, pixelDataB);
    const shapeSimilarity = calculateShapeSimilarity(pixelDataA, pixelDataB);
    
    // Комбинируем метрики с весами
    return 0.6 * mse + 0.4 * (1 - shapeSimilarity);
}

// Основная функция для анализа топ-10 кандидатов
function analyzeTopMatches() {
    console.log('Анализ топ-10 кандидатов с улучшенной точностью');
    
    // Имитация данных для примера
    const mockData = [
        { id: 1, mse: 789, contrast: 28, similarity: 0.92 },
        { id: 2, mse: 789, contrast: 28, similarity: 0.91 },
        { id: 3, mse: 795, contrast: 30, similarity: 0.89 },
        { id: 4, mse: 802, contrast: 32, similarity: 0.87 },
        { id: 5, mse: 812, contrast: 33, similarity: 0.85 },
        { id: 6, mse: 801, contrast: 31, similarity: 0.88 },
        { id: 7, mse: 805, contrast: 32, similarity: 0.86 },
        { id: 8, mse: 808, contrast: 32, similarity: 0.84 },
        { id: 9, mse: 810, contrast: 33, similarity: 0.83 },
        { id: 10, mse: 812, contrast: 33, similarity: 0.82 }
    ];
    
    // Сортируем по улучшенному коэффициенту схожести
    const sortedData = mockData.sort((a, b) => a.similarity - b.similarity);
    
    console.log('Результаты анализа:');
    sortedData.forEach((item, index) => {
        console.log(`#${index + 1} - ID: ${item.id}, MSE: ${item.mse}, Контрастность: ${item.contrast}, Схожесть: ${item.similarity.toFixed(2)}`);
    });
    
    console.log('Анализ завершен');
}

// Запуск анализа
analyzeTopMatches();