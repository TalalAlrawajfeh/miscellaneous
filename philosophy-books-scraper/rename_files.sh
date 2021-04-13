#!/bin/bash

cd out

files=$(ls)

for file in $files
do
    if [[ ! -f ${file}'.txt' ]]
    then
        gs -sDEVICE=txtwrite -dFirstPage=1 -dLastPage=1 -o ${file}.txt ${file}
    fi
done

python3 ../title_extractor.py > rename_files.sh

for file in $files
do
    rm  ${file}.txt
done

exit

chmod a+rwx rename_files.sh

. rename_files.sh

rm rename_files.sh
