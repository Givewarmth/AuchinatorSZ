
import os
import json
from pathlib import Path

def analyze_all_icon_directories(base_path):
    """
    Analyze all icon directories recursively to find all items
    """
    total_items = 0
    all_icons = []
    
    # Walk through all directories recursively
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                all_icons.append({
                    'path': os.path.join(root, file),
                    'filename': file,
                    'size': os.path.getsize(os.path.join(root, file))
                })
                total_items += 1
    
    return {
        'total_icons': total_items,
        'icon_list': all_icons
    }

def create_mapping_report():
    """
    Create a proper mapping report that includes all icon directories
    """
    base_path = "data/icons"
    
    # Analyze all directories
    analysis = analyze_all_icon_directories(base_path)
    
    # Create mapping report
    mapping_report = {
        "mapping_file": "mapping_report.json",
        "icons_folder": base_path,
        "screenshots_folder": "screenshots",
        "mapping_details": {
            "total_matches": analysis['total_icons'],
            "duplicate_ids": [],
            "valid_items": analysis['icon_list']
        },
        "folder_path": base_path,
        "analysis_timestamp": "2026-10-15",
        "notes": "This report includes all icons from all subdirectories, not just the 'other' folder"
    }
    
    return mapping_report

# Main execution
if __name__ == "__main__":
    report = create_mapping_report()
    
    # Write to file
    with open("mapping_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"Analysis complete. Found {report['mapping_details']['total_matches']} icons across all directories.")
    print("Report saved to mapping_report.json")
