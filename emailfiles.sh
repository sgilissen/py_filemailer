#!/bin/bash
# emailfiles.sh
# Uses a Python script to mail PDF files
# to a specified email address. 
LOG_FILE= # Logfile location
FILE_LOCATION= # Watch folder location
PROCESSED_FOLDER= # Folder to move the processed PDF files to

NOW=$(date +"%F %T.%N")


exec > >(tee -a ${LOG_FILE} )
exec 2> >(tee -a ${LOG_FILE} >&2)

for f in $FILE_LOCATION/*.pdf
do
	if [ -f "$f" ]; then
		fnm="$(basename -- $f)"
		echo "[$NOW] Processing file $f"
		python3 main.py $f <EMAILADDRESSHERE> # Change <EMAILADDRESSHERE> to the email address you want to send the file to
		echo "[$NOW] Moving file $f to $PROCESSED_FOLDER"
		mv $f $PROCESSED_FOLDER/$fnm
	else
		echo "[$NOW] No PDF files found."
	fi
done
echo "[$NOW] Finished processing all files."
echo "[$NOW] ------------------------------"
