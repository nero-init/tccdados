import pandas as pd

# Carregar o arquivo CSV para um DataFrame do pandas
csv_file = 'pesquisafim_unique_sem_duplicatas.csv'
df = pd.read_csv(csv_file)

# Escrever para um arquivo Excel
xlsx_file = 'pesquisafim_unique_sem_duplicatas.xlsx'
df.to_excel(xlsx_file, index=False, engine='openpyxl')

print(f'Arquivo Excel gerado com sucesso: {xlsx_file}')
