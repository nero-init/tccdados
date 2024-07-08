import json
import sqlite3

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def create_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS publicacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_publicacao TEXT,
            ano TEXT,
            titulo_obra TEXT,
            autores TEXT,
            link_href TEXT,
            publicacao TEXT,
            producao_nacional TEXT
        )
    ''')

def insert_data(cursor, data):
    for key, item in data.items():
        cursor.execute('''
            INSERT INTO publicacoes 
            (tipo_publicacao, ano, titulo_obra, autores, link_href, publicacao, producao_nacional) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            item['tipo_publicacao'],
            item['ano'],
            item['titulo_obra'],
            item['autores'],
            item['link_href'],
            item['publicacao'],
            item['producao_nacional']
        ))

def export_to_sql(input_file, output_file):
    data = load_json(input_file)
    
    conn = sqlite3.connect(output_file)
    cursor = conn.cursor()
    
    create_table(cursor)
    insert_data(cursor, data)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    input_file = "pesquisafim_unique_sem_duplicatas.json"
    output_file = "pesquisafim_unique_sem_duplicatas.db"  # Nome do arquivo do banco de dados SQLite
    
    export_to_sql(input_file, output_file)
    
    print(f"Dados exportados para o arquivo SQL: {output_file}")
