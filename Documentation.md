# CONVERSIONS DOCUMENTATION

## Converting an existing cha file to eaf. 

Use the `cha2eaf.py` script to convert an existing cha file to eaf. If the output 
option (`-o`) is not specified, the script will create a new eaf with the input 
file name as default. The script can be used as:

```
usage: cha2eaf.py [-h] [-o OUTPUT] cha_file
cha2eaf.py: error: the following arguments are required: cha_file

e.g.
python cha2eaf.py 01_06_sparse_code.cha
```

## Exporting a csv file from ELAN. 

Export a tab separated file with, then run the `awker.sh` file on the exported file. 


