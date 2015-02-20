#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

### this is done with the thought of producing descriptive stats for every feature.  Which one appear to be the most informative?

from sklearn import svm as SVM
import sys
import re
import os
import random
import numpy
import itertools
from constituency_features import *
from dependency_features import *
from vector_features import *



rootdir = sys.argv[1] ### marked_up

scores = []  ### do we need this



lemmas = LemmaFeatures(rootdir)
lemma_vector = lemmas.lemma_list

tri = PosTrigrams(rootdir)
tri_vector = tri.trigram_list



training = ['1'] # for only one iteration
train = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]  ### 'train' is a poor name here - there is no test data!

for fold in training:

    samples = []
    testing = []
    file_number = 1 ### remember to iterate from 1.
    
    
    for subdir, dirs, files in os.walk(rootdir): 
        
        if subdir:
            file_number = 1
            
        for f in files:

            this_file = (os.path.join(subdir, f))

            if file_number > 15:
                    pass
            
            elif 'dependencies' in this_file:

                features = []
                
                file_id = this_file.split('.')[-8].split('/')[-1]
                    
                
                text = open(this_file, 'r').readlines()
                
                words = WordFeatures(text)

                word_features = [words.findAgreementErrors, words.basicCountFeatures, words.getVerbFeatures, words.serEstar, 
                words.getCompoundTenses, words.getClitics, words.getNullSubjets]


                for feat in word_features:
                    f = feat()
                    if f:
                        for i in f:
                            features.append(i)
                
                weighted_lemma_vector = lemmas.makeWeightedVector(words.sentences)

                for i in weighted_lemma_vector:
                    features.append(i)

                weighted_pos_tri_vector = tri.getWeightedPosTrigram(words.sentences)

                for i in weighted_pos_tri_vector:
                    features.append(i)


                if file_number in train:
                    
                    samples.append(features); samples.append(file_id)
                    file_number += 1
                    
              
            
            elif 'freeling_parsed' in this_file:    
                print(this_file)
                file_id = this_file.split('.')[-5].split('/')[1]
                print('freeling id', file_id)
                    
                if file_id not in samples and file_id not in testing:
                    print('cant find it')
                    print('file_id', file_id)

                else:

                    text = open(this_file, 'r').readlines()
                    embedded = Embeddings(text)
                    count = embedded.countEmbeddings()
                    coord = embedded.getCoordinations()
                    
                    if file_id in samples:
                        
                        insert_here = samples.index(file_id) - 1
                        samples[insert_here].append(count)
                        samples[insert_here].append(coord)



    training_classes = []

    for s in samples:
        
        if type(s) == str:
            file_id = s
            if file_id .endswith('10') or file_id.endswith('9'):
                this_class = 'A'
            if file_id.endswith('13'):
                this_class = 'B'
            if file_id.endswith('U'):
                this_class = 'C'
            if file_id.endswith('N'):
                this_class = 'N'  
            training_classes.append(this_class)
            samples.remove(s)

    results = zip(training_classes, samples)
    

    A = []
    B = []
    C = []
    N = []

    for pair in results:
        label = pair[0]
        data = pair[1]
        if label == 'A':
            A.append(data)
        elif label == 'B':
            B.append(data)
        elif label == 'C':
            C.append(data)
        elif label == 'N':
            N.append(data)

    print('A ', A)
    print(sum(A)/len(A))

    print('B ', B)
    print(sum(B)/len(B))

    print('C ', C)
    print(sum(C)/len(C))

    print('N ', N)
    print(sum(N)/len(N))




        
        
            
            
            
            
            
            