#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from xml.etree import ElementTree
#from xml.dom.minidom import parseString




### 149-160-229-42:stanford-postagger-full-2014-08-27 danielwhyatt$ java -mx300m -classpath stanford-postagger-3.4.1.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/spanish.tagger -textFile '/Users/danielwhyatt/Downloads/C21NTV10N.text_only.txt' -outputFormat tsv 2> /dev/null > sample-tagged.txt 

import re
import sys
import os

infile = '/Users/danielwhyatt/Downloads/C21NTV10N.xml'

outfile = open(infile[0:-3] + 'text_only.txt', 'w')   ###/Users/danielwhyatt/Downloads/C21NTV10N.text_only.txt


# with open(infile, 'r') as f:

# 	for line in f:
# 		word = re.search('<w>(\w+)</w>', line)

# 		if line:
# 			if '<t type="p"/>' in line:
# 				print('.' + '\n' + '\n')
			
# 			elif 'type="retracing"' in line:
# 				pass

# 			else:
# 				if word:
# 					print(word.group(1) + '\n')




rootdir = sys.argv[1]  ### joe_lemmas_folder


for subdir, dirs, files in os.walk(rootdir):
	for f in files:

		if '.xml' in f:

			this_file = (os.path.join(subdir, f))
			print(this_file[:-3])
			

			#infile = open(this_file, 'r')   #.readlines()
			with open(this_file, 'r') as infile:
				outfile = open(this_file[0:-3] + 'text_only.txt', 'w') 
				for line in infile:
					#print(line)
					word = re.search('<w>(\w+)</w>', line)

					if line:

						if '<t type="p"/>' in line:

							outfile.write('.' + '\n' + '\n')

						elif 'type="retracing"' in line:
							pass

						else:
							if word:
								outfile.write(word.group(1) + '\n')	
				outfile.close()
							            
			
# 	soup = BeautifulSoup(f)
# 	# print(soup)


# print(soup.find_all('w'))

# linklist = [el.string for el in soup.findAll('w')]

# for l in linklist:
# 	print(l)


	#f = f.readlines()
		# print(line)

	# for line in f:
	# 	if line:
	# 		print(line)
		#	parseString(line)


# 	tree = ElementTree.parse(f)

# for node in tree.iter():
#     print(node.tag, node.attrib)

# node = tree.find('./with_attributes')
# print(node.tag)
# for name, value in sorted(node.attrib.items()):
#     print('  %-4s = "%s"' % (name, value))
# 	#dom = parseString(f)
# 	# data = dom.getElementsByTagName('w')[0].childNodes[0].data
# 	# print(data)


# for node in tree.iter():
	# print(node.tag, node.attrib)