# File Formats Report

## Working with ELAN

- Importing into ELAN works, but, when exporting the imported file back to CHAT:
	- participant codes are not imported (The meanings of MAN, etc. are lost from the header part of the CHAT file.
	- Some other metadata is also lost/changed
	- Timestamps get an %snd dependent tier annotation.
	- Some initial headers are lost, the ones that are there
	- @Eg, @Bg (pauses, conversations from lena) headers in the file are lost. I am not exactly sure if we use the info contained in these, which is important for possible solutions. 
	- Main line continuations cause issues after carriage return/newline. More specifically if we just continue a main line on the next line (at which point CLAN automatically adds a tab), ELAN messes it up. 

- Comments (such as skips, etc.) become dependent tiers, which is mostly not the case, hence we might wish to convert them to @Comment lines, and, for import into ELAN, their own tier. 

- No issues with "&=". These are just CLAN "simple events" (&=sneezes
 

## Possible Solution Routes/Scenarios

- If some of the info lost in the headers is not important, then I can write a short script to format CHAT files so that main info will not be lost (mainly the line continuations), and then we can use those.

- If we wish to retain some of the info in the headers (such as conversation starts and pauses, which come from LENA), I can write more code to bring them with us to ELAN as possibly an independent tier (or some other way)

- Conversion of existing files to ACLEW is not very simple, depending on what we wish to achieve, but is doable (we might wish to automatically track MWUs, etc.)

