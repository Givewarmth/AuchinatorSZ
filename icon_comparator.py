"""
Icon Comparator for Price Matching
"""

import cv2
import numpy as np
from PIL import Image
import json

def compare_icons(icon1, icon2):
    """Compare two icons using various methods"""
    # Simple pixel comparison
    if icon1.shape == icon2.shape:
        diff = np.sum(np.abs(icon1.astype(np.float32) - icon2.astype(np.float32)))
        return diff
    return float('inf')

def load_icon_mapping(mapping_file):
    """Load icon mapping from JSON file"""
    try:
        with open(mapping_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_icon_mapping(mapping, mapping_file):
    """Save icon mapping to JSON file"""
    with open(mapping_file, 'w') as f:
        json.dump(mapping, f, indent=2)

if __name__ == "__main__":
    print("Icon Comparator initialized")
