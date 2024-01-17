from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from urllib.request import urlopen

def downloadVideo(link, id):
    print(f"Baixando video {id} de: {link}")
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
        'id': link,
        'locale': 'en',
        'tt': 'a2pVYXRi',
    }
    
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

print("ETAPA 1: Abrindo Navegador")
options = Options()
options.add_argument("start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(options=options)
# Link da página
driver.get("https://www.tiktok.com/@cartok_ph")

# Necessário ajustar o delay para completar o captcha
time.sleep(30)

scroll_pause_time = 1
screen_height = driver.execute_script("return window.screen.height;")
i = 1

print("ETAPA 2: Carregando toda a página")
while True:
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    if (screen_height) * i > scroll_height:
        break 

# Classe da div que contem o elemento <a>
className = "css-1as5cen-DivWrapper"

script  = "let l = [];"
script += "document.getElementsByClassName(\""
script += className
script += "\").forEach(item => { l.push(item.querySelector('a').href)});"
script += "return l;"

urlsToDownload = driver.execute_script(script)

print(f"ETAPA 3: Inciando processo de download {len(urlsToDownload)} videos")
for index, url in enumerate(urlsToDownload):
    downloadVideo(url, index)
    time.sleep(10)