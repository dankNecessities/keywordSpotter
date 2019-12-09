#!/bin/bash
echo
echo "...... NORMALIZING AUDIOS ......."
echo

old_token_path="${kws}/old_tokens"
mkdir $old_token_path

# Get tokens
for i in $token_dir/*; do
	topdir="${old_token_path}/${i##*/}"
	mkdir $topdir
	for j in $i/*; do
		lowerdir="${topdir}/${j##*/}"
		mkdir $lowerdir
		folder="${j##*/}" && echo $folder
		if [ "$folder" = "test" ] || [ "$folder" = "train" ]; then
			for k in $j/*; do
				bottomdir="${lowerdir}"
				mkdir $bottomdir
				echo "${k%/*}" 
				echo $k
				echo $bottomdir
				eval "python3 $kws/scripts/py/normalizer.py -i $k -d 1"
				mv $k $bottomdir
				mv *.wav2 "${k%/*}"
			done
		fi
	done
done

echo
echo "...... NORMALIZING COMPLETE ....." 
echo
