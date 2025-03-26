import requests
from bs4 import BeautifulSoup
import time

import urllib

def scrape_url(url):
    try:
        #1. fazendo a requisição http
        print(f"Requisitando a url {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        response.raise_for_status() #faz a verificação se a requisição foi bem sucedida! (status 200)
        
        #2. Analisar o html com o BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        #3 Localizando os elementos com Dados
        # Aqui é onde será inspecionado o html da página para localizar os elementos que deseja extrair
        
        #Aqui estou localizando a div que contém a lista de resultados
        lista_resultados_div = soup.find('div', id='listaimoveispaginação')
        
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
                
                for item in itens_imoveis:
                    #extraindo informações de cada item
                    try:
                        info_li = item.select_one('li.form-row.clearfix')
                        Titulo = "Titulo não encontrado"
                        numero_imovel = None
                        numero_item = None
                        endereco = None
                        observacoes = None
                        
                        if info_li:
                            info_span = info_li.select_one('div.control-item span')
                            if info_span:
                                linhas = [p.strip() for p in info_span.get_text("\n").split('\n') if p.strip()]
                                if linhas:
                                    titulo = linhas[0] if len(linhas) > 0 else "Titulo não encontrado"
                                    if len(linhas) > 1 and "Número do imóvel :" in linhas[1]:
                                        numero_imovel = linhas[1].split(":")[1].strip()
                                    if len(linhas) > 2 and "Número do item :" in linhas[2]:
                                        numero_item = linhas[2].split(":")[1].strip()
                                    if len(linhas) > 3:
                                        endereco = linhas[3].strip()
                                    if len(linhas) > 4:
                                        observacoes = linhas[4].strip()
                                      
                        #Imagem fica dentro do li anterior
                        imagem_tag = item.select_one("div.fotoimovel-col1 > img")
                        imagem_url = imagem_tag.get('src') if imagem_tag and imagem_tag.get('src') else None
                        imagem_completa = urllib.parse.urljoin(website_data['baseUrl'], imagem_url) if imagem_url else None 
                        
                        # Link para detalhes (dentro do segundo <li>)
                        link_detalhes = None
                        link_tag = item.select_one('li.form-row.clearfix:nth-child(2) a[onclick^="javascript:detalhe_imovel("]')
                        if link_tag and link_tag.get('onclick'):
                            import re
                            match = re.search(r'detalhe_imovel\((\d+)\)', link_tag.get('onclick'))
                            if match:
                                imovel_id = match.group(1)
                                link_detalhes = f"{website_data['baseUrl']}/detalhes.asp?id={imovel_id}"
                                
                        dados_imovel = {
                            'titulo': titulo,
                            'imagem': imagem_completa,
                            'link_detalhes': link_detalhes,
                            'preco': None,  # Ensure 'preco' is defined or replace with actual logic
                            'numero_imovel': numero_imovel,
                            'numero_item': numero_item,
                            'endereco': endereco,
                            'observacoes': observacoes,
                            # Adicione outros campos que você deseja extrair aqui
                        }
                        dados_imoveis.append(dados_imovel)
                    
                    except Exception as e:
                        print(f"Erro ao extrair informações do item: {e}")
                        continue
            return dados_imoveis
        else:
            print("Lista de resultados não encontrada")
            return []
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a requisição: {e}")
        return None
    except Exception as e:
        print(f"ocorreu um erro ao processar a página")

if __name__ == "__main__":
    target_url = "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp"  # Substitua por a URL real do site
    dados = scrape_url(target_url)

    if dados:
        print("\nDados dos Imóveis:")
        for imovel in dados:
            print(imovel)
    else:
        print("\nNão foi possível obter os dados dos imóveis.")