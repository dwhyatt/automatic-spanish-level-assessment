#!/bin/bash

myvar=$(find -d current_folder -name "*text_only.txt" -type f)

for i in $myvar; do
    echo $i 
    cat $i | iconv -f utf-8 -t ISO8859-1 | FREELINGSHARE=/opt/local/share/freeling  analyze -f /opt/local/share/freeling/config/es.cfg --outf shallow | iconv -f ISO8859-1 -t utf-8 > $i'.freeling_parsed.txt'
done