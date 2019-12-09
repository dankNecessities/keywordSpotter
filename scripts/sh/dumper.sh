#!/bin/bash
echo
echo "...... GETTING NUMPY DUMPS ......."
echo

if [ "$1" = "--keep-old" ]; then
	mkdir $kws/dumped
	mv "${kws}/tokens/*" "${kws}/dumped"
	echo "*****Old dumps retained.*****"
else
	rm -rf "${data_dir}/*"
fi

# Convert tokens to numpy dumps
for i in $tmp_dir/*; do
	name="${i##*/}" && echo $name
	file_dir="${data_dir}/${name}"
	mkdir $file_dir && echo $file_dir
	for j in $i/*; do
		folder="${j##*/}" && echo $folder
		if [ "$folder" = "test" ] || [ "$folder" = "train" ]; then
			inner_dir="${file_dir}/${folder}"
			mkdir $inner_dir
			for k in $j/*; do
				eval "python3 ${kws}/scripts/py/mel_converter.py -i $k -n ${name} -s"
				mv *"${name}"* $inner_dir
			done
		fi
	done
done

rm -rf $tmp_dir

echo
echo "...... DUMPING COMPLETE ......."
echo
