"""
Icon Price Matcher for Auction System
"""

import json
import os

class IconPriceMatcher:
    def __init__(self, mapping_file='mapping.json'):
        self.mapping = self.load_mapping(mapping_file)
    
    def load_mapping(self, mapping_file):
        """Load icon to price mapping"""
        try:
            with open(mapping_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def match_icon_to_price(self, icon_name):
        """Match icon to its price"""
        return self.mapping.get(icon_name, None)
    
    def add_mapping(self, icon_name, price):
        """Add new icon to price mapping"""
        self.mapping[icon_name] = price
        self.save_mapping()
    
    def save_mapping(self, mapping_file='mapping.json'):
        """Save mapping to file"""
        with open(mapping_file, 'w') as f:
            json.dump(self.mapping, f, indent=2)
    
    def get_all_mappings(self):
        """Get all current mappings"""
        return self.mapping

if __name__ == "__main__":
    print("Icon Price Matcher initialized")
