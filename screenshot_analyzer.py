"""
Screenshot Analyzer for Icon Detection
"""

import cv2
import numpy as np
from PIL import Image
import os

def detect_icons_in_screenshot(screenshot):
    """Detect icons in screenshot"""
    # Convert to grayscale
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    icon_positions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # Filter out small contours
        if w > 10 and h > 10:
            icon_positions.append((x, y, w, h))
    
    return icon_positions

def analyze_screenshot(screenshot):
    """Complete analysis of screenshot"""
    icon_positions = detect_icons_in_screenshot(screenshot)
    return {
        'icon_positions': icon_positions,
        'total_icons': len(icon_positions)
    }

if __name__ == "__main__":
    print("Screenshot Analyzer initialized")
