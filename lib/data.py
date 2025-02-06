import os.path
from queue import Queue

VERSION = "1.0.0"

AUTHOR = "seaung"

ROOT_PATHS = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../"))

POCS_PATHS = os.path.join(ROOT_PATHS, "pocs")

OUTPUT_PATHS = os.path.join(ROOT_PATHS, "output")

POCS = []

WORKER = Queue()

CONF = {}

class PocResult:
    def __init__(self, vuln_name="", payload="", msg="", poc_name="", vuln_url="", status=False):
        self.vuln_name = vuln_name
        self.payload = payload
        self.msg = msg
        self.poc_name = poc_name
        self.vuln_url = vuln_url
        self.status = status

    def to_dict(self):
        return {
            "vuln_name": self.vuln_name,
            "payload": self.payload,
            "msg": self.msg,
            "poc_name": self.poc_name,
            "vuln_url": self.vuln_url,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        return PocResult(
            vuln_name=data.get("vuln_name", ""),
            payload=data.get("payload", ""),
            msg=data.get("msg", ""),
            poc_name=data.get("poc_name", ""),
            vuln_url=data.get("vuln_url", ""),
            status=data.get("status", False)
        )
