import argparse


def set_commandline_options():
    usage = "Ipcsuite [options]"

    parser = argparse.ArgumentParser(prog="Ipcsuite", usage=usage)

    parser.add_argument("-v", "--version", dest="version", action="store",
                       help="show version", type=str)
    parser.add_argument("-t", "--target", dest="target", action="store",
                        help="Target URL (e.g.) 192.168.1.0", type=str)
    parser.add_argument("-o", "--output", dest="output", action="store",
                        help="Output data to file", type=str)
    parser.add_argument("-fx", "--format", dest="format", action="store",
                       help="")

    return parser.parse_args(), parser

