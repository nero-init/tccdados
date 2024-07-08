import json
import os

def merge_json_files(input_files, output_file):
    all_data = {}
    current_id = 0
    
    for file in input_files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for key in data:
                all_data[current_id] = data[key]
                current_id += 1
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Lista dos arquivos de entrada
    input_files = [f"{year}.json" for year in range(2013, 2023)]
    output_file = "uniao.json"
    
    merge_json_files(input_files, output_file)
    print(f"Dados unificados foram salvos em {output_file}")
