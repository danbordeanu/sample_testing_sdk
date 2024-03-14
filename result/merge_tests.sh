#!/usr/bin/env bash
# AUTHOR:   metropolis
# FILE:     merge_tests.sh
# ROLE:     TODO (some explanation)
# CREATED:  2017-11-15 16:37:58
# MODIFIED: 2017-11-16 11:13:22


DIR_in=../html
declare list="$(\ls -A1 "$DIR_in"| grep html)"

#filename=`date +%Y-%d-%H-%I-%S`
#filename+='.html'
filename='index.html'

cp "header.txt" "$filename"

for FILE in $list; do 
    if [[ $FILE == *"multiple"* ]]; then
        echo "not adding $FILE"
        #echo "adding: " $FIL 
        #cat "../html/$FILE"  | sed  '/TABLE/d' >> "$filename"
    else
        echo "adding: " $FILE
        cat "../html/$FILE"  | sed  '/TABLE/d' >> "$filename"
    fi

done

echo "</TABLE> " >> "$filename"


#firefox "$filename"
#rm $filename
