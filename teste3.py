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
    imoveis_data: [List[Dict]] = []
    url = f"{website_data['baseUrl']}"
    print(f"Requisitando a url {url}")
    
    try:
        #inicializando o webdriver
        service = Service()
        
        driver = webdriver.Chrome(service=service)
        driver.get(url)

        time.sleep(5) #tempo para a pagina carregar
        
        #Agora começa a interação com a página
        select_State = driver.find_element(By.ID, "cmb_estado")
        select1 = Select(select_State)
        select1.select_by_visible_text("SP")

        time.sleep(5)
            
        select_city = driver.find_element(By.ID, "cmb_cidade")
        selectCity = Select(select_city)
        selectCity.select_by_visible_text("SAO PAULO")


        time.sleep(3)
        btn_next = driver.find_element(By.ID, "btn_next0")
        btn_next.click()

        time.sleep(3)

        # select_TipoImovel = driver.find_element(By.ID, "cmb_tp_imovel")
        # select2 = Select(select_TipoImovel)
        # select2.select_by_visible_text("Apartamento")
        # time.sleep(3)
        # select_valorImovel = driver.find_element(By.ID, "cmb_faixa_vlr")
        # select3 = Select(select_valorImovel)
        # select3.select_by_index(3)
        # time.sleep(3)

        btn_next2 = driver.find_element(By.ID, "btn_next1")
        btn_next2.click()
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 40).until(lambda driver:any(
            "carregaListaImoveis.asp" in request.url and request.response 
            for request in driver.requests
        ))
        
        for request in driver.requests:
            if "carregaListalmoveis.asp" in request.url and request.response:
                response_body = request.response.body.decode('utf-8')
                data = json.loads(response_body)
                # Extrair os dados dos imóveis do JSON
                # ... seu código para extrair os dados do JSON ...
                break
        
        time.sleep(5)
        
        #1. fazendo a requisição http
        html_content = driver.page_source
        #print(f"html passado", html_content)
        #2. Analisar o html com o BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        print(f"cheguei aqui")
        #3 Localizando os elementos com Dados
        # Aqui é onde será inspecionado o html da página para localizar os elementos que deseja extrair
        
        #Aqui estou localizando a div que contém a lista de resultados
            
        lista_resultados_div = soup.find('div', className='wrapper')
        print(lista_resultados_div)
        dados_imoveis = []
        
        
        if lista_resultados_div:
            #agora será necessário buscar dentro desta div para localizar os elementos que deseja extrair
            #a abordagem mais comum é localizar todos os <ul>s dentro da div
            listas_ul = lista_resultados_div.find_all('ul', class_='control-group no-bullets')
            
            for ul in listas_ul:
                #localizando os elementos dentro do <ul> que deseja extrair
                #aqui é onde será inspecionado o html da página para localizar os elementos que deseja extrair
                #e extrair os dados
                itens_imoveis = ul.find_all('li', class_ = 'group-block-item')
                print(f"cheguei nessa parte 1")
                
                for item in itens_imoveis:
                    
                    foto_imovel = item.find_all('div', class_ = 'fotoimovel-col1')
                    print(f"cheguei nessa parte 2")
                    
                    for fotinha in foto_imovel:
                        #localizando a imagem do imovel
                        imagem_tag = fotinha.find_all('img', class_ = 'fotoimovel')
                        
                        print(f"cheguei nessa parte 3")
                        if imagem_tag:
                            for imagem_tag in image_tag:
                                image_url = imagem_tag.get('src')
                                print(f"Imagem URL: {image_url}")
                                print(f"cheguei nessa parte 4")
                            # Aqui você pode fazer o download da imagem ou armazená-la como desejar
                        else:
                            print("Imagem não encontrada")
                            
                    #extraindo informações de cada item
                    # try:
                    #     info_li = item.select_one('li.form-row.clearfix')
                    #     Titulo = "Titulo não encontrado"
                    #     numero_imovel = None
                    #     numero_item = None
                    #     endereco = None
                    #     observacoes = None
                        
                    #     if info_li:
                    #         info_span = info_li.select_one('div.control-item span')
                    #         if info_span:
                    #             linhas = [p.strip() for p in info_span.get_text("\n").split('\n') if p.strip()]
                    #             if linhas:
                    #                 titulo = linhas[0] if len(linhas) > 0 else "Titulo não encontrado"
                    #                 if len(linhas) > 1 and "Número do imóvel :" in linhas[1]:
                    #                     numero_imovel = linhas[1].split(":")[1].strip()
                    #                 if len(linhas) > 2 and "Número do item :" in linhas[2]:
                    #                     numero_item = linhas[2].split(":")[1].strip()
                    #                 if len(linhas) > 3:
                    #                     endereco = linhas[3].strip()
                    #                 if len(linhas) > 4:
                    #                     observacoes = linhas[4].strip()
                                      
                    #     #Imagem fica dentro do li anterior
                    #     imagem_tag = item.select_one("div.fotoimovel-col1 > img")
                    #     imagem_url = imagem_tag.get('src') if imagem_tag and imagem_tag.get('src') else None
                    #     imagem_completa = urllib.parse.urljoin(website_data['baseUrl'], imagem_url) if imagem_url else None 
                        
                    #     # Link para detalhes (dentro do segundo <li>)
                    #     link_detalhes = None
                    #     link_tag = item.select_one('li.form-row.clearfix:nth-child(2) a[onclick^="javascript:detalhe_imovel("]')
                    #     if link_tag and link_tag.get('onclick'):
                    #         import re
                    #         match = re.search(r'detalhe_imovel\((\d+)\)', link_tag.get('onclick'))
                    #         if match:
                    #             imovel_id = match.group(1)
                    #             link_detalhes = f"{website_data['baseUrl']}/detalhes.asp?id={imovel_id}"
                                
                    #     dados_imovel = {
                    #         'titulo': titulo,
                    #         'imagem': imagem_completa,
                    #         'link_detalhes': link_detalhes,
                    #         'preco': None,  # Ensure 'preco' is defined or replace with actual logic
                    #         'numero_imovel': numero_imovel,
                    #         'numero_item': numero_item,
                    #         'endereco': endereco,
                    #         'observacoes': observacoes,
                    #         # Adicione outros campos que você deseja extrair aqui
                    #     }
                    #     dados_imoveis.append(dados_imovel)
                    
                    # except Exception as e:
                    #     print(f"Erro ao extrair informações do item: {e}")
                    #     continue
            return dados_imoveis
        else:
            print("Lista de resultados não encontrada")
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