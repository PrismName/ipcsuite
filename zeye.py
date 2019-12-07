import time

from lib.data import VERSION, AUTHOR
from lib.cmd import set_commandline_options


def banner():
    logo = """
       _                   _ __
      (_)__  _______ __ __(_) /____
     / / _ \/ __(_-</ // / / __/ -_)
    /_/ .__/\__/___/\_,_/_/\__/\__/
   /_/
            {} #dev

            {}
    """.format(VERSION, AUTHOR)
    print(logo)


def init():
    pass


def start():
    pass


def worker():
    pass


def end():
    print("[*] end shutdown {0}".format(time.strftime("%X")))


def main():
    banner()
    init()
    start()
    end()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
