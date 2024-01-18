# importações do Python
import requests
from time import sleep
from random import randint
from urllib.request import urlopen
from functools import partial

# Importações de Bibliotecas Externas
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.remote.switch_to import SwitchTo
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# Importações Internas 
...

def baixaVideo(link, id):
    """
    Realiza download do vídeo via https://ssstik.io/.
        
    :param link: A url do vídeo do TikTok.
    :param id: O Id do vídeo (Será utilizado como nome do arquivo).
    """

    # cURL para requisição de download
    # Caso ocorra algum erro no processo de download abaixo, é necessário atualizar estes valores cfme exemplificado na documentação
    cookies = {
        '_ga': 'GA1.1.1557075317.1705533096',
        '__gads': 'ID=6482fd4e2c52e2b0:T=1705533095:RT=1705533095:S=ALNI_MaQyI3ZpyZT7EqnaFVZkpIf49PQfA',
        '__gpi': 'UID=00000db81388497a:T=1705533095:RT=1705533095:S=ALNI_MZdx-BoolGXazutejb1Ta9NUCoKwQ',
        '_ga_ZSF3D6YSLC': 'GS1.1.1705533096.1.0.1705533124.0.0.0',
    }
    headers = {
        'authority': 'ssstik.io',
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '_ga=GA1.1.1557075317.1705533096; __gads=ID=6482fd4e2c52e2b0:T=1705533095:RT=1705533095:S=ALNI_MaQyI3ZpyZT7EqnaFVZkpIf49PQfA; __gpi=UID=00000db81388497a:T=1705533095:RT=1705533095:S=ALNI_MZdx-BoolGXazutejb1Ta9NUCoKwQ; _ga_ZSF3D6YSLC=GS1.1.1705533096.1.0.1705533124.0.0.0',
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
        'id': link, # Esta é a URL do vídeo à ser baixado, não é necessário atualizar..
        'locale': 'en',
        'tt': 'a2pVYXRi',
    }
    

    print(f"Baixando video {id} de: {link}")
    print("ETAPA 4: Buscando o link para download")
    print("Caso a etapa 4 dê erro, é necessário verificar cookies, headers, params e data")
    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    downloadSoup = BeautifulSoup(response.text, "html.parser")

    downloadLink = downloadSoup.a["href"]
    videoTitle = downloadSoup.p.getText().strip()

    print("ETAPA 5: Salvando o vídeo")
    mp4File = urlopen(downloadLink)
    with open(f"videos/{id}.mp4", "wb") as output:
        while True:
            data = mp4File.read(4096)
            if data:
                output.write(data)
            else:
                break

def aguardaElemento(driver, by, value=str):
    """
    Aguarda o carregamento do elemento.
    """
    def espera(by, element, webdriver):
        return bool(webdriver.find_elements(by, element))
    
    espera_webdriver = WebDriverWait(driver, 10)
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

    # Abrindo página do TikTok
    driver.get("https://www.tiktok.com/")

    try:
        # Aguardando pela tela de login
        aguardaElemento(driver, By.XPATH, '/html/body/div[5]/div[3]/div/div/div/div[1]/div/div/div[3]/div/div')
        print("Encontrou botão de 'Continuar sem login'")
        bt_sem_login = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div/div[1]/div/div/div[3]/div/div')
        print("Guardou o elemento bt_sem_login")
        espera_aleatoria(valor_inicial=2,valor_final=4)
        print("Aguardou aleatoriamente")
        # Pelo action.click não estava funcionando, portanto decidi clicar via JavaScript
        driver.execute_script("document.querySelector('.css-u3m0da-DivBoxContainer').click();")
        print("Clicou no elemento")
    except:
        # É possível que o Tiktok não solicite login..
        ...

    # Navegando para o perfil escolhido
    driver.get("https://www.tiktok.com/@cartok_ph")

    # Nessa etapa é possível que o TikTok apresente um CAPTCHA
    # Caso necessário, habilite esse sleep e resolva manualmente.
    # sleep(30)

    # Dando Scroll até o final da página
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1

    print("ETAPA 2: Carregando toda a página")
    while True:
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        espera_aleatoria(3,5)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        if (screen_height) * i > scroll_height:
            break 

    # Classe da div que contem o elemento <a>
    className = "css-1as5cen-DivWrapper"

    # Montando script para listar as Urls dos vídeos
    script  = "let l = [];"
    script += "document.getElementsByClassName(\""
    script += className
    script += "\").forEach(item => { l.push(item.querySelector('a').href)});"
    script += "return l;"

    # Executando Script
    urlsDosVideos = driver.execute_script(script)

    print(f"ETAPA 3: Inciando processo de download {len(urlsDosVideos)} videos")
    for i, url in enumerate(urlsDosVideos):
        baixaVideo(url, i)
        espera_aleatoria(10,12) # Espera de 10 à 12s para iniciar o próximo download