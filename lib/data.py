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
