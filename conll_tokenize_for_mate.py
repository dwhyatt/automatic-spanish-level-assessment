#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
rootdir = sys.argv[1]


for subdir, dirs, files in os.walk(rootdir):
	for f in files:
		
		this_file = (os.path.join(subdir, f))
		
		if this_file.endswith('text_only.txt'):
			print(this_file)
			o = open(this_file, 'r') #.readlines()
			outfile = open(this_file + '.conll', 'w')
			x = 1
			for line in o:
				word = line.strip()
				
				if word:
					outfile.write(str(x) + '\t' + word + '\t' + '_' + '\t' + '_' + '\t' + '_' + '\t' + '_' + '\t' + '_' + '\t' + '_' + '\t' + '_' + '\t' + '_' + '\t' + '_' + '\t' + '_' + '\t' + '_' + '\n')
					x += 1
				else:
					outfile.write('\n')
					x = 1
			
			outfile.close()