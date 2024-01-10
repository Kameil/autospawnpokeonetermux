import requests
import subprocess
import os
from termcolor import colored

def download_file(url, file_name):
    print('Procurando atualizações...')
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, "w") as file:
            file.write(response.text)
        return True
    return False

github_url = "https://raw.githubusercontent.com/Kameil/autospawnpokeonetermux/main/bot.py"
local_file_name = "bot.py" 



if download_file(github_url, local_file_name):
    try:
        subprocess.run(["python3", local_file_name], check=True)
    except subprocess.CalledProcessError:
        print(colored('Erro ao executar o arquivo.', "red"), colored(' Entre em contato com o discord', 'yellow'))
      
else:
    print(colored('Não foi possível baixar o bot.', 'red'), colored('\n entre em contato com o discord ou:', 'yellow'), colored('\npossiveis soluções: \n • da fork denovo\n • verificar se nao apagou o codigo sem querer apertando no botao history.\n • Tentar Novamente mais tarde.', 'green'))
