import argparse
from signal import signal, SIGPIPE, SIG_DFL

import pympi as pym

# Just set the default signal to be able to pipe the output.
signal(SIGPIPE, SIG_DFL)

def set_args():
    """Sets command line arguments. """

    parser = argparse.ArgumentParser(description="Convert EAF (ELAN) file to  CHA (CLAN) file")
    parser.add_argument('eaf_file', help='The EAF file to be converted')
    parser.add_argument(
        '-o', '--output',
        help='The output CHA file name. Optional, default is the input file name.',
        default=''
    )
    return parser.parse_args()


def eaf2cha(inpf, outf):
    eaf = pym.Elan.Eaf(inpf)

    return eaf



if __name__ == "__main__":
    args = set_args()

    eaf = eaf2cha(args.eaf_file, args.output)
