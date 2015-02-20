#!/usr/bin/env bash

myvar=$(find -d current_folder -name "*.conll" -type f)

for i in $myvar; do
    echo $i
    java -Xmx3G -cp anna-3.3.jar is2.lemmatizer.Lemmatizer -model CoNLL2009-ST-Spanish-ALL.anna-3.3.lemmatizer.model -test $i -out $i'.lemmas'
	java -Xmx3G -cp anna-3.3.jar is2.tag.Tagger -model CoNLL2009-ST-Spanish-ALL.anna-3.3.postagger.model -test $i'.lemmas' -out $i'.coursetags' 
	java -Xmx3G -cp anna-3.3.jar is2.parser.Parser -model CoNLL2009-ST-Spanish-ALL.anna-3.3.parser.model -test $i'.coursetags' -out $i'.dependencies.txt' 
	rm $1
	rm $1'lemmas'
	rm $1'coursetagged'
done
