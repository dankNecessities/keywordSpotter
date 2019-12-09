#SHELL SCRIPT THAT RENAMES FILES IN A FOLDER AS THE FOLDER NAME PLUS AN INDEX

itempath=$(pwd)
extension=".wav"
echo $itempath

for i in $itempath/*; do
	#echo "$i"
	if [ "$i" = "${itempath}/renamer.sh" ]; then
		echo "N"
	else
		indexcount=0
		for j in $i/*; do
			z="${i}/${i##*/}_${indexcount}_renamed${extension}"
			echo $j
			echo $z
			mv "$j" "$z"
			#echo $indexcount
			indexcount=$(($indexcount + 1))
		done
	fi
done
