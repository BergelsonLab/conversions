import pympi
import pyvyu

import argparse


def _set_args():
    parser = argparse.ArgumentParser(description='Convert opf and cha files to eaf')
    parser.add_argument('-o', '--output', help='Name of the output file. Default will be the same name with the extension changed appropriately')
    parser.add_argument('input', help='The cha/opf file to convert')
    return parser.parse_args()

if __name__ == "__main__":
    args = _set_args()
    eaf_object = pympi.Elan.eaf_from_chat(args.input)
    eaf_object.to_file('test.eaf')

    

