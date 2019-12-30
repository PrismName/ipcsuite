class Colors:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    FUCHSIA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    RESET = "\033[0m"

    def colors(self, color, string):
        return f"{getattr(self, color)}{string}{self.RESET}"

    def red(self, string):
        return self.colors("RED", string)

    def green(self, string):
        return self.colors("GREEN", string)

    def yellow(self, string):
        return self.colors("YELLOW", string)

    def blue(self, string):
        return self.colors("BLUE", string)

    def fuchsia(self, string):
        return self.colors("FUCHSIA", string)

    def cyan(self, string):
        return self.colors("CYAN", string)

    def white(self, string):
        return self.colors("WHITE", string)

