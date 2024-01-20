# importações do Python
import requests
from time import sleep
from random import randint
from urllib.request import urlopen
from functools import partial

# Importações de Bibliotecas Externas
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

# Importações Internas 
...

def baixaVideo(id, propriedades_video):
    """
    Realiza download do vídeo via https://ssstik.io/.
        
    :param link: A url do vídeo do TikTok.
    :param id: O Id do vídeo (Será utilizado como nome do arquivo).
    """
    link = propriedades_video['url']
    views = propriedades_video['views']
    perfil = propriedades_video['perfil']

    # cURL para requisição de download
    # Caso ocorra algum erro no processo de download abaixo, é necessário atualizar estes valores cfme exemplificado na documentação
    cookies = {
        '_ga': 'GA1.1.1557075317.1705533096',
        '__gads': 'ID=6482fd4e2c52e2b0:T=1705533095:RT=1705715697:S=ALNI_MaQyI3ZpyZT7EqnaFVZkpIf49PQfA',
        '__gpi': 'UID=00000db81388497a:T=1705533095:RT=1705715697:S=ALNI_MZdx-BoolGXazutejb1Ta9NUCoKwQ',
        '_ga_ZSF3D6YSLC': 'GS1.1.1705715697.6.0.1705715706.0.0.0',
    }

    headers = {
        'authority': 'ssstik.io',
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '_ga=GA1.1.1557075317.1705533096; __gads=ID=6482fd4e2c52e2b0:T=1705533095:RT=1705715697:S=ALNI_MaQyI3ZpyZT7EqnaFVZkpIf49PQfA; __gpi=UID=00000db81388497a:T=1705533095:RT=1705715697:S=ALNI_MZdx-BoolGXazutejb1Ta9NUCoKwQ; _ga_ZSF3D6YSLC=GS1.1.1705715697.6.0.1705715706.0.0.0',
        'hx-current-url': 'https://ssstik.io/en',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/en',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'NnZBMVVk',
    }
    
    print("ETAPA 4: Buscando o link para download ssstik")
    print("Caso a etapa 4 dê erro, é necessário verificar cookies, headers, params e data")
    retorno = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    download_soup = BeautifulSoup(retorno.text, "html.parser")

    link_download = download_soup.a["href"]
    # titulo_video = download_soup.p.getText().strip()

    print("ETAPA 5: Salvando o vídeo")
    video = urlopen(link_download)
    with open(f"videos/{id}_{int(views)}_{perfil}.mp4", "wb") as output:
        while True:
            data = video.read(4096)
            if data:
                output.write(data)
            else:
                break

def aguardaElemento(driver, by, value=str, tempo=10):
    """
    Aguarda o carregamento do elemento.
    """
    def espera(by, element, webdriver):
        return bool(webdriver.find_elements(by, element))
    
    espera_webdriver = WebDriverWait(driver, tempo)
    espera_webdriver.until(partial(espera, by, value))

def espera_aleatoria(valor_inicial=1, valor_final=3):
    """
    Espera um tempo aleatório (em segundos).
    
    :param valor_inicial: O primeiro valor da aleatoriedade (int).
    :type valor_inicial: int
    :param valor_final: O último valor da aleatoriedade (int).
    :type valor_final: int
    """
    return sleep(randint(valor_inicial, valor_final))

def converter_views(str_views):
    if 'K' in str_views:
        return float(str_views.replace('K', '').replace(',', '')) * 1000
    elif 'M' in str_views:
        return float(str_views.replace('M', '').replace(',', '')) * 1000000
    else:
        return float(str_views.replace(',', ''))

def carrega_toda_pagina(driver):
    # Inicializa a altura atual da página
    ultima_altura = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll até o final da página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        espera_aleatoria(valor_inicial=5, valor_final=7)

        nova_altura = driver.execute_script("return document.body.scrollHeight")

        # Se a altura não mudou, chegou ao final
        if nova_altura == ultima_altura:
            break

        ultima_altura = nova_altura

def pula_login(driver):
    try:
        # Aguardando pela tela de login
        aguardaElemento(driver, By.XPATH, '/html/body/div[5]/div[3]/div/div/div/div[1]/div/div/div[3]/div/div')
        print("Encontrou botão de 'Continuar sem login'")
        #bt_sem_login = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div/div[1]/div/div/div[3]/div/div')
        #print("Guardou o elemento bt_sem_login")
        espera_aleatoria(valor_inicial=2,valor_final=4)
        print("Aguardou aleatoriamente")
        # Pelo action.click não estava funcionando, portanto decidi clicar via JavaScript
        driver.execute_script("document.querySelector('.css-u3m0da-DivBoxContainer').click();")
        print("Clicou no elemento")
    except:
        # É possível que o Tiktok não solicite login..
        ...   


if __name__ == '__main__':

    print("ETAPA 1: Abrindo Navegador")

    # Configs para o driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-popup-block')
    chrome_options.add_argument("no-default-browser-check")
    chrome_options.add_argument("--enable-automation")
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument("--incognito")

    driver = webdriver.Chrome(chrome_options)
    action = ActionChains(driver)

    lista_paginas = ['https://www.tiktok.com/@cartok_ph']
    limite_videos = 5
    for pagina in lista_paginas:
        # Abrindo página do TikTok
        #driver.get("https://www.tiktok.com/")
        #pula_login(driver)

        driver.get(pagina)
        pula_login(driver)

        if pagina.find('@'):
            nome_perfil = pagina[pagina.find('@') + 1:]

        # Nessa etapa é possível que o TikTok apresente um CAPTCHA
        # Caso necessário, habilite esse sleep e resolva manualmente.
        # sleep(30)

        # Dando Scroll até o final da página
        carrega_toda_pagina(driver)

        # Classe da div que contém o elemento <a>
        classe_div = "css-1as5cen-DivWrapper"

        # Montando script para listar as URLs dos vídeos e valores da tag <strong>
        script  = "let data = [];"
        script += f"document.getElementsByClassName(\"{classe_div}\").forEach(item => {{"
        script +=     "let url = item.querySelector('a').href;"
        script +=     "let countElement = item.querySelector('.video-count');"
        script +=     "let countText = countElement ? countElement.innerText : '0';"
        script +=     "data.push({url, countText});"
        script += "});"
        script += "return data;"

        # Executando Script
        listaVideos = driver.execute_script(script)
        for i, data in enumerate(listaVideos):
            listaVideos[i]['countText'] = converter_views(data['countText'])
        print(listaVideos)

        # Ordenando a lista
        listaVideos.sort(key=lambda x: x['countText'], reverse=True)

        driver.quit()

        print(f"ETAPA 3: Iniciando processo de download {len(listaVideos)} vídeos")
        contador = 0
        for i, data in enumerate(listaVideos):
            contador = contador + 1
            if (contador < limite_videos):
                print(f"Iniciando download do vídeo {data['url']} que possui {int(data['countText'])} views")
                propriedades_video = {'url': data['url'], 'views': data['countText'], 'perfil': nome_perfil}
                baixaVideo(i, propriedades_video)
                espera_aleatoria(8, 14)  # Espera de 10 a 12s para iniciar o próximo download
