#!/usr/bin/env python3
import json
import sys

def merge_json_files(file1, file2, output_file):
    """
    Merge two JSON files with the same structure by combining their 'models' objects.
    
    Args:
        file1: Path to the first JSON file
        file2: Path to the second JSON file
        output_file: Path to save the merged JSON file
    """
    try:
        # Load the two JSON files
        with open(file1, 'r') as f1:
            data1 = json.load(f1)
        
        with open(file2, 'r') as f2:
            data2 = json.load(f2)
        
        # Check if both files have the expected structure
        if 'models' not in data1 or 'models' not in data2:
            print("Error: One or both files do not have the expected 'models' structure.")
            return False
        
        # Create a new data structure with merged models
        merged_data = {"models": {}}
        
        # Copy models from the first file
        for model, model_data in data1['models'].items():
            merged_data['models'][model] = model_data
        
        # Copy models from the second file (will overwrite if there are duplicates)
        for model, model_data in data2['models'].items():
            merged_data['models'][model] = model_data
        
        # Write the merged data to the output file
        with open(output_file, 'w') as f_out:
            json.dump(merged_data, f_out, indent=2)
        
        print(f"Successfully merged {file1} and {file2} into {output_file}")
        
        # Count models
        print(f"Number of models in merged file: {len(merged_data['models'])}")
        print(f"  - Models from {file1}: {len(data1['models'])}")
        print(f"  - Models from {file2}: {len(data2['models'])}")
        
        return True
    
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python merge_json.py <file1.json> <file2.json> <output.json>")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output_file = sys.argv[3]
    
    success = merge_json_files(file1, file2, output_file)
    sys.exit(0 if success else 1)