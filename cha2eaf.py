from sys import stdout, stderr
import argparse
from signal import signal, SIGPIPE, SIG_DFL
from os import path

import pympi as pym
import pyclan

import pdb

# Just set the default signal to be able to pipe the output.
signal(SIGPIPE, SIG_DFL)

# Participant dictionary, may become useful later, but currently not used.
P_DICT = {}

# Properties dictionary, used to check uniqueness of property keys. This is
# not mandatory, but the forums suggest this: https://tla.mpi.nl/topic/embed-metadata-in/
PROP_DICT = {}

# Dictionaries for LENA conversation and pause header information.
CONV_DICT = {}
PAUS_DICT = {}

TEMP_LIST = []
# Some string constants from CHAT files for ease of use.
PARTICIPANTS = '@Participants:'
BG = '@Bg:'
EG = '@Eg:'

# Other helpful constants, some defined by EAF specification, some by me. 
SYMAC = 'Symbolic_Association'
# linguistic type name for dependent tiers. I just picked this name, unlike
# the constant above, which is a definition necessary for pympi.
DEPENDENT = 'dependent' 

COM = '%com'
XCOM = '%xcom'
XDB = '%xdb'
BLOCK = 'block'


def set_args():
    """Sets command line arguments. """

    parser = argparse.ArgumentParser(description="Convert CHA (CLAN) file to EAF (ELAN) file")
    parser.add_argument('cha_file', help='The CHA file to be converted')
    parser.add_argument(
        '-o', '--output',
        help='The output EAF file name. Optional, default is the input file name.',
        default=''
    )
    return parser.parse_args()

def process_line(line, eaf):
    """Process a line from the CHA file"""

    prop_dict = dict(eaf.get_properties())
    
    # Checking for empty line
    if not line:
        return

    # Case where the line is a header line.
    elif line.startswith('@'):

        # Process participants header. 
        if line.startswith(PARTICIPANTS):

            # A list of participants in the form: ['SIL Silence LENA', ' MAN Male_Adult_Near Male', ...] 
            participants = line.replace(PARTICIPANTS, '').strip().split(',')

            # Key value pair for the eaf property header element. 
            key = PARTICIPANTS
            value = '\n'.join([i.strip() for i in participants])

            # Adding the participants to the eaf property element
            if key not in prop_dict:
                eaf.add_property(key, value)

            for par in participants:
                P_DICT[par.strip().split()[0]] = par.strip()

        elif line.startswith((EG, BG)):
            return

    # Line is a main tier. 
    elif line.startswith("MAIN"):
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
        stderr.write('Found a multiline!\n')
        new_line = ' '.join(llist)
        stderr.write(new_line + '\n')
        return new_line

def setup_eaf():
    """Initial setup of the eaf filne is handled here to reduce complexity."""
    eaf = pym.Elan.Eaf()

    eaf.add_linguistic_type(
            XDB, 
            constraints=SYMAC, 
            timealignable=False
            )

    eaf.add_linguistic_type(
            COM, 
            constraints=SYMAC, 
            timealignable=False
            )

    eaf.add_linguistic_type(
            XCOM, 
            constraints=SYMAC, 
            timealignable=False
            )

    eaf.add_tier(
            BLOCK
            )
    return eaf

def _process_header(cha, eaf):

    buf = []

    # Processing the header. TODO: Extract to a function
    for linum, line in enumerate(cha.get_header()):
        # If line is either a header, main tier, or dependent tier:
        if line.line.startswith(('@', '*', '%')):
            # If buffer has content
            new_line = process_buf(buf)
            buf.clear()
            process_line(new_line, eaf)
        # If line is none of the above, we assume that it is a continuation!
        buf.append(line.line.strip())

def add_ref_annotation(line, eaf):
    # lines of the form '%com:\t|BC|1|0|0|XIOCA|NT|FI|\n'
    # Doing these modifications here so as to not break pyclan elsewhere
    # in case that breaks something.

    name = line.tier + '@' + line.parent_tier
    if name not in eaf.get_tier_names():
        eaf.add_tier(
                tier_id = name,
                ling = line.tier,
                parent = line.parent_tier
                )

    eaf.add_ref_annotation(
            name,
            line.parent_tier,
            (line.onset + line.offset)/2,
            line.content)

def cha2eaf(inpf, outf):
    """Converts a given cha file to an eaf file. """

    eaf = setup_eaf()
    cha = pyclan.ClanFile(inpf)
    participants = {}

    # Currently not returning anything, but might return a participant database in the future?
    _process_header(cha, eaf)

    # Processing the rest of the file after the header.
    end = cha.get_header()[-1].index

    current_tier = ''
    # The plus one below starts the iteration right after the last header line.
    for line in cha.line_map[end+1:]:
        # This is a tier line.
        if line.is_tier_line:
            # If the tier does not exist, add it first. 
            if line.tier not in eaf.get_tier_names():
                eaf.add_tier(line.tier)

            current_tier = line.tier

        elif line.is_paus_block_delimiter or line.is_conv_block_delimiter:
            line.tier = BLOCK
            line.content = line.line.strip()

            # pympi does not like onset and offset being the same...
            if line.onset == 0 and line.offset == 0:
                line.onset, line.offset = 0, 1

            else:
                line.onset += 1
                line.offset -= 1
    
        elif line.is_clan_comment or line.is_user_comment or 'xcom' in line.line:
            line.parent_tier = line.tier if line.tier in eaf.get_tier_names() else current_tier
            line.tier, line.content = line.line.strip().split('\t')
            add_ref_annotation(line, eaf)
            continue

        elif line.xdb_line:
            line.tier = XDB

            # Usually XDB lines do get parent_tier set from pyclan, but if there are 
            # other lines in between, that does not appear to be the case. So we are 
            # setting it here.
            if not line.parent_tier:
                line.parent_tier = current_tier
            add_ref_annotation(line, eaf)
            continue

        elif line.is_end_header:
            # This is just the end header. It is not necessary to add it.
            continue

        else:
            print(line)
            print('UNPROCESSED LINE ABOVE')
            continue


        last_annotation = (line.tier, line.onset, line.offset, line.content)
        eaf.add_annotation(*last_annotation)

    # If no output file option is supplied. 
    if outf == '':
        outf = path.basename(inpf).replace('.cha', '.eaf')

    eaf.to_file(outf)

if __name__ == "__main__":
    args = set_args()
    cha2eaf(args.cha_file, args.output)
