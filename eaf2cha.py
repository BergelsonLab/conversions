import argparse
from signal import signal, SIGPIPE, SIG_DFL
from operator import itemgetter

import pympi as pym

# Just set the default signal to be able to pipe the output.
#signal(SIGPIPE, SIG_DFL)

def set_args():
    """Sets command line arguments. """

    parser = argparse.ArgumentParser(description="Convert EAF (ELAN) file to  CHA (CLAN) file")
    parser.add_argument('eaf_file', help='The EAF file to be converted')
    parser.add_argument(
        '-o', '--output',
        help='The output CHA file name. Optional, default is the input file name.',
        default='default_output_file.cha'
    )
    return parser.parse_args()

def eaf2cha(inpf, outf):
    eaf = pym.Elan.Eaf(inpf)
    return eaf

if __name__ == "__main__":
    args = set_args()

    eaf = eaf2cha(args.eaf_file, args.output)

    output = list()
    for tier in eaf.get_tier_names():
        end_time = eaf.timeslots['ts{}'.format(eaf.maxts)]
        for annots in eaf.get_annotation_data_between_times(tier, 0, end_time):
            annots = *annots, tier
            output.append(annots)

    print(output)
    output.sort(key=itemgetter(0,1))
    print(output)

    file_out = []
    for item in output:
        # Block line: @Bg Pause 1, @Eg etc.
        if item[-1] == 'block':
            line = '{}'.format(item[2])

        # process the xdb lines.
        elif item[-1].startswith('%xdb'):
            line = '%xdb:\t{}'.format(item[2])

        #comment lines. These can be merged with xdb above for conciseness.
        elif item[-1].startswith('%com'):
            line = '%com:\t{}'.format(item[2])

        elif item[-1].startswith('%xcom'):
            line = '%com:\t{}'.format(item[2])

        #process the main tier lines.
        elif item[-1].isupper():
            line = '*{}:\t{}\x15{}_{}\x15'.format(item[-1], item[2], item[0], item[1])


        print(line)
        file_out.append(line)

    for i in range(len(file_out)-1):
        if 'Bg' in file_out[i] and 'Eg' in file_out[i+1]:
            file_out[i], file_out[i+1] = file_out[i+1], file_out[i]


    
    with open(args.output, 'w') as of:
        of.write('\n'.join(file_out))
















