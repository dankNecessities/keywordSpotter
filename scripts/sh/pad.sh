#!/bin/bash
echo
echo "...... PADDING TOKENS ......."
echo

if [ "$1" = "--delete-old" ]; then
	del=true
fi

# Get tokens
for i in $token_dir/*; do
	tok_dir="${tmp_dir}/${i##*/}" && echo $tok_dir
	if ! $del; then
		# Needs to be repositioned
		# rm -rf "$label_dir"
		echo ""
	fi
	mkdir "$tok_dir"
	for j in $i/*; do
		folder="${j##*/}" && echo $folder
		if [ "$folder" = "test" ] || [ "$folder" = "train" ]; then
			mkdir "${tok_dir}/${folder}"
			for k in $j/*; do
				eval "python3 $kws/scripts/py/padder.py -i $k -l 1000"
				mv *pad_* "${tok_dir}/${folder}"
				mv *trim_* "${tok_dir}/${folder}"
			done
		fi
	done
done

echo
echo "...... PADDING COMPLETE ......."
echo
