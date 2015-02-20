# -*- coding: UTF-8- -*-
#!/bin/env python3.4

import os

class LemmaFeatures:

    def __init__(self, rootdir): 
        self.rootdir = rootdir
        self.lemma_list = self.makeLemmaList()
        


    def makeLemmaList(self):  ### this should only be called once at top of document

        lem_list = []

        for subdir, dirs, files in os.walk(self.rootdir):
            #print('subdir', subdir)
            for f in files:
                  
                if 'dependencies' in f:

                    this_file = (os.path.join(subdir, f))
                    
                    infile = open(this_file, 'r').readlines()
                    
                    for line in infile:
                        line = line.split('\t')
                        
                        if len(line) == 14:
                           
                            word = line[1]
                            lemma = line[3]
                            
                            if lemma not in lem_list:
                                lem_list.append(lemma)
        return lem_list

    def makeWeightedVector(self, sentences):

        this_file_vector = {}

        for sent in sentences:
            for line in sent:
                lemma = line[3]

                if lemma in this_file_vector:
                    this_file_vector[lemma] += 1
                else:
                    this_file_vector[lemma] = 1
                
        out_vector = []
            
        for word in self.lemma_list:
            if word in this_file_vector.keys():
                out_vector.append(this_file_vector[word])
            else:
                out_vector.append('0')
                
        return out_vector

class PosTrigrams:

    def __init__(self, rootdir):
        
        self.rootdir = rootdir
        self.trigram_list = self.makePosTrigramList()

 
    def makePosTrigramList(self):

        tri_list = []
        rootdir = self.rootdir

        for subdir, dirs, files in os.walk(rootdir):
            for f in files:

                if 'dependencies' in f:

                    this_file = (os.path.join(subdir, f))
                    
                    infile = open(this_file, 'r').readlines()

                    tags = []
                    for line in infile:
                        line = line.split('\t')
                        if len(line) == 14:
                            tags.append(line[5])

                    t_grams = trigrams(tags)

                    for tri in t_grams:   

                        if tri not in tri_list:
                            tri_list.append(tri)
        return tri_list
       

    def getWeightedPosTrigram(self, sentences):
        
        these_pos = []

        for sent in sentences:
            for line in sent:
                these_pos.append(line[5])

        these_trigrams = trigrams(these_pos)
        these_trigrams = (str(tri) for tri in these_trigrams)

        this_file_vector = {}

        for tri in these_trigrams:

            if tri in this_file_vector:
                this_file_vector[tri] += 1
            else:
                this_file_vector[tri] = 1
            
        out_vector = []
        
        for tri in self.trigram_list:
            
            if tri in this_file_vector.keys():
                out_vector.append(this_file_vector[tri])
              
            else:
                out_vector.append('0')
        
        return out_vector

