from sys import stdout, stderr
import argparse
from signal import signal, SIGPIPE, SIG_DFL
from os import path

import pympi as pym
import pyclan

# Just set the default signal to be able to pipe the output.
signal(SIGPIPE, SIG_DFL)

# Participant dictionary, may become useful later, but currently not used.
P_DICT = {}

# Properties dictionary, used to check uniqueness of property keys. This is not mandatory, but the forums suggest this: https://tla.mpi.nl/topic/embed-metadata-in/
PROP_DICT = {}

# Dictionaries for LENA conversation and pause header information.
CONV_DICT = {}
PAUS_DICT = {}

TEMP_LIST = [] 
# Some string constants from CHAT files for ease of use. 
PARTICIPANTS = '@Participants:'
BG = '@Bg:'
EG = '@Eg:'
   
def set_args():
    """Sets command line arguments. """

    parser = argparse.ArgumentParser(description="Convert CHA (CLAN) file to EAF (ELAN) file")
    parser.add_argument('cha_file', help='The CHA file to be converted')
    parser.add_argument('-o', '--output', help='The output EAF file name. Optional, default is the input file name.', default='')
    return parser.parse_args()

def process_line(line, eaf):
    """Process a line from the CHA file"""

    prop_dict = dict(eaf.get_properties())
    
    # Checking for empty line
    if not line:
        return

    # Case where the line is a header line.
    elif line.startswith('@'):
        stdout.write('Processing header line\n')

        # Process participants header. 
        if line.startswith(PARTICIPANTS):
            stdout.write('Processing Participants header\n')

            # A list of participants in the form: ['SIL Silence LENA', ' MAN Male_Adult_Near Male', ...] 
            participants = line.replace(PARTICIPANTS, '').strip().split(',')

            # Key value pair for the eaf property header element. 
            key = PARTICIPANTS
            value = '\n'.join([i.strip() for i in participants])

            stdout.write(value + '\n')

            # Adding the participants to the eaf property element
            if key not in prop_dict:
                eaf.add_property(key, value)

            for par in participants:
                P_DICT[par.strip().split()[0]] = par.strip()

        elif line.startswith((EG, BG)):
            return

    # Line is a main tier. 
    elif line.startswith(MAIN):
        llist = line.strip().split()

def process_buf(llist):
    """Processes the buffer to form a coherent line that will be processed. """

    if not llist:
        return

    # Just return the single line.
    elif len(llist) == 1:
        return llist[0]

    # Format the possible multiline! 
    else:
        stderr.write('Found a multiline!')
        new_line = ' '.join(llist)
        stderr.write(new_line)
        return new_line


def cha2eaf(inpf, outf):
    """Converts a given cha file to an eaf file. """

    eaf = pym.Elan.Eaf()
    cha = pyclan.ClanFile(inpf)
    participants = {}
    buf = []
    for linum, line in enumerate(cha.get_header()):
        # If line is either a header, main tier, or dependent tier:
        if line.line.startswith(('@', '*', '%')):
            # If buffer has content
            new_line = process_buf(buf)
            buf.clear()
            process_line(new_line, eaf)
        # If line is none of the above, we assume that it is a continuation!
        buf.append(line.line.strip())

    # Processing the rest of the file after the header.
    end = cha.get_header()[-1].index
    for line in cha.line_map[end:]:
        # This is a tier line.
        if line.is_tier_line:
            # If the tier does not exist, add it first. 
            if line.tier not in eaf.get_tier_names():
                eaf.add_tier(line.tier)

            eaf.add_annotation(line.tier, line.onset, line.offset, line.content)

    # If no output file option is supplied. 
    if outf == '':
        outf = path.basename(inpf).replace('.cha', '.eaf')

    eaf.to_file(outf)

if __name__ == "__main__":
    args = set_args()
    cha2eaf(args.cha_file, args.output)
