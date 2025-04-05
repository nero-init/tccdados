from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import threading
import os

# Função para extrair dados da página atual
def extrair_dados(driver, id_counter):
    elements = driver.find_elements(By.XPATH, "//div[@class='col-md-12' and starts-with(@id, 'conteudo')]")
    data = {}

    for element in elements:
        try:
            element_id = f"conteudo-{id_counter}"
            id_counter += 1

            ano = element.find_element(By.XPATH, ".//p[2]/b[1]").text
            tipo_publicacao = element.find_element(By.XPATH, ".//div[1]/div/p/b").text
            titulo_obra = element.find_element(By.CLASS_NAME, "titulo-busca").text
            autor_element = element.find_elements(By.XPATH, './p[1]/b')
            autor = autor_element[0].text if autor_element else ""
            link_element = element.find_element(By.XPATH, './/div[3]/div[1]/a')
            link_href = link_element.get_attribute('href')
            publicacao = element.find_element(By.XPATH, "./p[2]/b[2]").text

            data[element_id] = {
                "tipo_publicacao": tipo_publicacao,
                "ano": ano,
                "titulo_obra": titulo_obra,
                "autores": autor,
                "link_href": link_href,
                "publicacao": publicacao
            }

            print(f"ID: {element_id}, Autor: {autor}, Ano: {ano}, Tipo de publicação: {tipo_publicacao}, Título Publicação: {titulo_obra}, Publicado: {publicacao}, Link Href: {link_href}")
        except Exception as e:
            print(f"Erro ao processar elemento: {e}")

    return data, id_counter

# Função para obter o número total de páginas
def obter_numero_paginas(driver):
    pagination_elements = driver.find_elements(By.XPATH, '//ul[@class="pagination"]/li/span[@class="page-link page-buscador"]')
    if pagination_elements:
        return max([int(e.get_attribute("data-page")) for e in pagination_elements])
    else:
        return 1

# Função para clicar em uma página específica
def clicar_pagina(driver, numero_pagina):
    try:
        page_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//ul[@class="pagination"]/li/span[@class="page-link page-buscador" and @data-page="{numero_pagina}"]'))
        )
        page_button.click()
        return True
    except Exception as e:
        print(f"Erro ao clicar na página {numero_pagina}: {e}")
        return False

def monitorar_input(driver, id_counter, arquivo_json):
    while True:
        comando = input("Digite 'forcepage' para capturar os dados da página atual ou 'sair' para encerrar: ") #por algum motivo a paginação nao conta a ultima pagina, a seguir de 9. sendo necessário acessar a ultima pagina e rodar o comando.
        if comando == "forcepage":
            data, id_counter = extrair_dados(driver, id_counter)
            if os.path.exists(arquivo_json):
                with open(arquivo_json, "r", encoding="utf-8") as json_file:
                    all_data = json.load(json_file)
            else:
                all_data = {}
            all_data.update(data)
            with open(arquivo_json, "w", encoding="utf-8") as json_file:
                json.dump(all_data, json_file, indent=4, ensure_ascii=False)
        elif comando == "sair":
            break

def main():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    #url = "https://www-periodicos-capes-gov-br.ezl.periodicos.capes.gov.br/index.php/acervo/buscador.html?q=concepts%3Ablockchain+OR+cryptocurrency&mode=advanced"
    url = "https://www.periodicos.capes.gov.br/index.php/acervo/buscador.html?q=all%3Acontains%28blockchain%29+OR+all%3Acontains%28crypto%29&mode=advanced&source=all"
    driver.get(url)
    driver.implicitly_wait(2)

    anoinit = input("Digite o ano inicial: ")
    anofim = input("Digite o ano final: ")
    
    all_data = {}
    id_counter = 0
    arquivo_json = f"{anoinit}.json"

    try:
        input_ano_inicial = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="collapse-publish_year"]/input[1]'))
        )
        input_ano_inicial.clear()
        input_ano_inicial.send_keys(anoinit)

        input_ano_final = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="collapse-publish_year"]/input[2]'))
        )
        input_ano_final.clear()
        input_ano_final.send_keys(anofim)
        
        filtro_ano_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="filtro-ano"]/i'))
        )
        filtro_ano_icon.click()

        time.sleep(4)

        num_paginas = obter_numero_paginas(driver)

        for pagina in range(1, num_paginas + 1):
            if pagina > 1:
                if not clicar_pagina(driver, pagina):
                    break
                time.sleep(2)

            page_data, id_counter = extrair_dados(driver, id_counter)
            all_data.update(page_data)

        with open(arquivo_json, "w", encoding="utf-8") as json_file:
            json.dump(all_data, json_file, indent=4, ensure_ascii=False)

        threading.Thread(target=monitorar_input, args=(driver, id_counter, arquivo_json)).start()

    finally:
        print(f"Foram registrados até então {id_counter} resultados, referente a {num_paginas} páginas.s")

main()
