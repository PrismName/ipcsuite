import argparse


def set_commandline_options():
    usage = "Ipcsuite [options]"

    parser = argparse.ArgumentParser(prog="Ipcsuite", usage=usage)

    parser.add_argument("-v", "--version", dest="version", action="store_true",
                       help="show version", default=False)
    parser.add_argument("-t", "--target", dest="target", action="store",
                        help="Target URL (e.g.) 192.168.1.0", type=str)
    parser.add_argument("-o", "--output", dest="output", action="store",
                        help="Output data to file", type=str)
    parser.add_argument("-f", "--format", dest="format", action="store",
                        help="Output format (json/txt/html)", type=str, default="txt")
    parser.add_argument("-n", "--threads", dest="threads", action="store",
                        help="Number of threads to use", type=int, default=10)
    parser.add_argument("-T", "--timeout", dest="timeout", action="store",
                        help="Request timeout in seconds", type=int, default=30)
    parser.add_argument("-d", "--debug", dest="debug", action="store_true",
                        help="Enable debug mode", default=False)

    return parser.parse_args(), parser

