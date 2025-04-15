import requests
from bs4 import BeautifulSoup
import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import ssl
from typing import List, Dict, Optional

context = ssl.SSLContext()
context.verify_mode = ssl.CERT_NONE

def scrape_data_with_selenium(website_data: Dict) -> List[Optional[Dict]]:
    imoveis_data = []
    url = f"{website_data['baseUrl']}"
    print(f"Requisitando a url {url}")
    
    service = Service()
    driver = webdriver.Chrome(service=service)
    
    try:
        #inicializando o webdriver
        driver.get(url)
        
        wait = WebDriverWait(driver, 10)

        # Selecionar Estado
        select_estado = wait.until(EC.presence_of_element_located((By.ID, "cmb_estado")))
        Select(select_estado).select_by_visible_text("SP")

        time.sleep(2)
        
        # Selecionar Cidade
        select_cidade = wait.until(EC.presence_of_element_located((By.ID, "cmb_cidade")))
        Select(select_cidade).select_by_visible_text("SAO PAULO")

        time.sleep(4)

        # Próximo passo
        btn_next = wait.until(EC.element_to_be_clickable((By.ID, "btn_next0")))
        btn_next.click()

        time.sleep(2)

        # Segundo botão de próximo
        btn_next2 = wait.until(EC.element_to_be_clickable((By.ID, "btn_next1")))
        btn_next2.click()

        time.sleep(2)

        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 40).until(lambda driver:any(
            "carregaListaImoveis.asp" in request.url and request.response 
            for request in driver.requests
        ))
        
        for request in driver.requests:
            if "carregaListaImoveis.asp" in request.url and request.response:
                response_body = request.response.body.decode('utf-8', errors='ignore')
                soup = BeautifulSoup(response_body, "html.parser")
                
                print(soup.prettify())
                
                
                # Exemplo: coletar blocos de imóveis
                imovel_blocks = soup.find_all("div", id_="listaImoveisPaginacao")
                for block in imovel_blocks:
                        
                    lista_ul = block.find("ul", class_="no-bullets")
                    
                    for lista in lista_ul:
                        
                        lista_li = lista.find("li", class_="group-block-item")
                        
                        for infos in lista_li:
                                            
                            foto = infos.find("div", class_="fotoimovel-col1")
                            imovel = {
                                "foto": foto.text.strip() if foto else None,
                            }
                            imoveis_data.append(imovel)
                            print(f"imovel", imovel)
                        break  # só pega a primeira requisição válida
        return []
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a requisição: {e}")
        return None
    except Exception as e:
        print(f"ocorreu um erro ao processar a página", e)

if __name__ == "__main__":
    website_info = {
        "baseUrl": "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp", # Substitua pela URL real
    }
    
    resultados = scrape_data_with_selenium(website_info)

    if resultados:
        print("\nDados dos Imóveis:")
        for imovel in dados:
            print(imovel)
    else:
        print("\nNão foi possível obter os dados dos imóveis.")