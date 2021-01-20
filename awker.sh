#!/bin/sh

awk '

BEGIN { 
	print "tier,word,utterance_type,object_present,speaker,annotid,timestamp,basic_level,comment";
	regex="([A-Za-z]*\\+)*[A-Za-z]+ *&=[a-z]_[a-z]_[A-Z1]{3}_0x[a-f0-9]{6}";
	OFS=",";
}
{ 
	tier="*" $1
	timestamp=$2 "_" $3;
	annot=""
	# The loop below concatenates the annotation part of the line.
	for (i=5; i<=NF; i++) {
		annot=annot " " $i;
	}


	while (match(annot,regex)) {
		extract=substr(annot, RSTART, RLENGTH);
		annot=substr(annot, RSTART+RLENGTH);
		search =" ";
		n=split(extract, array, search);
		word=array[1];
		annotation=substr(array[2], 3);
		search="_";
		n=split(annotation, array, search);
		utt=array[1];
		obj=array[2];
		speaker=array[3];
		annotid=array[4];
		print tier, word, utt, obj, speaker, annotid, timestamp, " ", "NA";
	}
}

'

