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

Below are the steps to export a csv file from ELAN that will be in the style of sparse code csv files. If the options section gets confusing, just follow along with the attached images.

1. Click file in the upper left corner.
	![]()
2. Select `Export as` from the dropdown menu.
3. Select `Tab-delimited text` from the dropdown menu. 
4. Check/Uncheck the following options (All of these are also shown in the picture, in case this is hard to follow):
	- Select (if not already selected) `By Tier Names` from the `Select tiers` section at the top. You should see a list of the usual chat file tiers (`CXF`, `NOF`, `CHF`, etc.).
	- Select `Show only root tiers` below the tier names window. This will hide away all the dependent tiers (such as `%xdb@OLN`)
	- **Uncheck** the default and block tiers (if these don't exist in your file, that is fine). The main point is that we are making sure that we are only taking tiers that have 3 letter names.  
	- Under the `Output options` section, select `Exclude participant names from output` option.
	- Under the `Include time column for` section, check the boxes for `Begin Time` and `End Time`. 
	- Under the `Include time format` section, check the box for msec option (which stands for milliseconds).
5. Click `OK` to export :) . You will get a text file of tab separated values.
6. The resulting file is still not a csv (comma separated values) file. Run the script `awker.sh` as `./awker.sh < newly_exported_tab_separated_file.txt`. This is a short `awk` script that will turn the exported file you just obtained into a sparse code csv file that we have been using. 

