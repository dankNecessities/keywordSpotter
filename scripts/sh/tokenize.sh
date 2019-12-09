#!/bin/bash
echo
echo "....... TOKENIZING AUDIOS ........."
echo

tmp="$tokenize_audio_path/tmp"
mkdir $tmp
cd $tmp
for i in $tokenize_audio_path/*; do
	echo "tokenizing $i"
	tok="${i%.*}"
	echo $tok
	stok="${tok#"$tokenize_audio_path/"}"
	echo $stok
	mkdir $tok
	eval 'auditok -e 55 -m 2 -i $i -o "$stok"_{N}_{start}_{end}.wav'
	mv *$stok* $tok
	mv $tok $tokenize_path
done

rm -rf "$tokenize_path/tmp"
rm -rf "$tokenize_path/wav"

echo
echo "....... TOKENIZING COMPLETE ......."
echo 
