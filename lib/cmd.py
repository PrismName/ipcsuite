import argparse


def set_commandline_options():
    usage = "Ipcsuite [options]"

    parser = argparse.ArgumentParser(prog="Ipcsuite", usage=usage)

    parser.add_argument("-v", "--version", dest="version", action="store_true",
                       help="show version", type=str)
    parser.add_argument("-t", "--target", dest="target", action="store_true",
                        help="Target URL (e.g.) 192.168.1.0", type=str)

    return parser

