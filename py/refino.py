import json
import re

def clean_publicacao(data):
    for key in data:
        if 'publicacao' in data[key]:
            original_publicacao = data[key]['publicacao']
            cleaned_publicacao = re.sub(r'[^a-zA-Z0-9]', '', original_publicacao[:4]) + original_publicacao[4:]
            data[key]['publicacao'] = cleaned_publicacao
    return data

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        cleaned_data = clean_publicacao(data)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    input_file = "uniao.json"
    output_file = "uniao_cleaned.json"
    
    process_file(input_file, output_file)
    print(f"Arquivo processado e salvo como {output_file}!")
