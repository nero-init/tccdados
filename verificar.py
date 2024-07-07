import json
from collections import defaultdict

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def find_duplicates(data, key):
    seen = set()
    duplicates = defaultdict(list)
    
    for item_key, item in data.items():
        value = item.get(key)
        if value in seen:
            duplicates[value].append(item_key)
        else:
            seen.add(value)
    
    return duplicates

if __name__ == "__main__":
    pesquisafim_file = "pesquisafim.json"
    
    pesquisafim_data = load_json(pesquisafim_file)
    
    # Encontrar exemplos de duplicatas em link_href
    duplicates_link_href = find_duplicates(pesquisafim_data, 'link_href')
    print(f"Exemplos de duplicatas em link_href:")
    count_link_href = 0
    for value, keys in duplicates_link_href.items():
        if count_link_href >= 3:
            break
        print(f"Valor: {value}, Chaves: {keys}")
        count_link_href += 1
    
    # Encontrar exemplos de duplicatas em titulo_obra
    duplicates_titulo_obra = find_duplicates(pesquisafim_data, 'titulo_obra')
    print(f"\nExemplos de duplicatas em titulo_obra:")
    count_titulo_obra = 0
    for value, keys in duplicates_titulo_obra.items():
        if count_titulo_obra >= 3:
            break
        print(f"Valor: {value}, Chaves: {keys}")
        count_titulo_obra += 1
