import json
from collections import defaultdict

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def find_duplicate_pairs(data):
    duplicate_pairs = defaultdict(list)
    
    # Percorre os dados para encontrar pares duplicados de titulo_obra e autores
    seen_pairs = set()
    for key, item in data.items():
        titulo_autores_pair = (item['titulo_obra'], item['autores'])
        
        # Verifica se o par já foi visto
        if titulo_autores_pair in seen_pairs:
            duplicate_pairs[titulo_autores_pair].append(key)
        else:
            seen_pairs.add(titulo_autores_pair)
    
    return duplicate_pairs

if __name__ == "__main__":
    pesquisafim_unique_file = "pesquisafim_unique_sem_duplicatas.json"
    
    # Carrega os dados do arquivo JSON
    pesquisafim_unique_data = load_json(pesquisafim_unique_file)
    
    # Encontra pares duplicados de titulo_obra e autores
    duplicate_pairs = find_duplicate_pairs(pesquisafim_unique_data)
    
    # Conta e lista os pares duplicados encontrados
    num_duplicates = sum(len(keys) for keys in duplicate_pairs.values() if len(keys) > 1)
    
    if num_duplicates > 0:
        print(f"Foram encontrados {num_duplicates} pares de titulo_obra e autores iguais:")
        for pair, keys in duplicate_pairs.items():
            if len(keys) > 1:
                print(f"Par: {pair}, Chaves: {keys}")
    else:
        print("Não foram encontrados pares de titulo_obra e autores iguais.")
