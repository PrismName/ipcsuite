from lib.data import VERSION, AUTHOR


def banner():
    logo = """
       _                   _ __
      (_)__  _______ __ __(_) /____
     / / _ \/ __(_-</ // / / __/ -_)
    /_/ .__/\__/___/\_,_/_/\__/\__/
   /_/
            {}

            {}
    """.format(VERSION, AUTHOR)
    print(logo)


def main():
    banner()


if __name__ == "__main__":
    main()
