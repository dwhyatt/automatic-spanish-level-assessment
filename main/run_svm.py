#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-


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

rootdir = sys.argv[1] 

scores = [] 



# def randomSplit():
#     train = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]   ### 15 is the cut-off as some files (native speakers) only have 15 files.  But it would be to somehow use the 
#                                                     ### extra data in cases where its available.
#     x = 0
#     while x < 3: 
#         i = random.choice(train)
#         train.remove(i)
#         x += 1

#     return train

# training = []
# i = 0
# while i < 10:
#     training.append(randomSplit())



lemmas = LemmaFeatures(rootdir)
lemma_vector = lemmas.lemma_list


tri = PosTrigrams(rootdir)
tri_vector = tri.trigram_list


training = ['1']
train = [1]
#train = [1,2,3,4,5,6,7,8,9,10,11,12]

for fold in training:   ##### 'training' here would be 10 iterations of random splits

    samples = []
    testing = []
    file_number = 1 
    
    
    for subdir, dirs, files in os.walk(rootdir): 
        
        if subdir:
            file_number = 1
            
        for f in files:

            this_file = (os.path.join(subdir, f))

            if file_number > 15:
                    pass
            
            elif 'dependencies' in this_file:

                features = []
                
                file_id = this_file.split('.')[-8].split('/')[-1]   ### parsed from end so it can be moved
                    
                
                text = open(this_file, 'r').readlines()
                
                words = WordFeatures(text)

                word_features = [words.findAgreementErrors, words.basicCountFeatures, words.getVerbFeatures, words.serEstar, 
                words.getCompoundTenses, words.getClitics, words.getNullSubjets, words.getVerbBasics]


                for feat in word_features:  ### what is returned from each call should be iterable.
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
                    
                    
                else:
                    testing.append(features); testing.append(file_id)
                    file_number += 1
            
            elif 'freeling_parsed' in this_file:    
                
                file_id = this_file.split('.')[-5].split('/')[1]   ### should match file_id from dependencies files
                print('freeling id', file_id)
                    
                if file_id not in samples and file_id not in testing:   ### this should always match, we might want to add and exception here.
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

                    elif file_id in testing:

                        insert_here = testing.index(file_id) - 1
                        testing[insert_here].append(count)
                        testing[insert_here].append(coord)


    training_classes = []

    for s in samples:   #### this turn the file_ids into the CEF levels so they can be evaluated...
        
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

    gold_classes = []

    for s in testing:
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
            gold_classes.append(this_class)
            testing.remove(s)

      
    print(samples, training_classes)
    for s in samples:
        print(len(s))
    print(testing, gold_classes)
    for t in testing:
        print(len(t))
    ####lin_clf = svm.LinearSVC()
    ####lin_clf.fit(samples, training_classes)

    clf = SVM.SVC()
    clf.fit(samples, training_classes)

    i = 0
    r = 0; w = 0

    while i < len(testing):
       
        prediction = str(clf.predict([testing[i]]))
        print('prediction', prediction)
        while t < len(gold_classes):
            golden = str(gold_classes[i])
            if golden in prediction:
                
                r += 1
                t += 1
                break
            else:
                
                w += 1
                t += 1
                break

    accuracy = r/(r+w)
    scores.append(accuracy)
    

#print(scores)

#results = list(zip(scores, combinations))
#print(results)
print(scores)
#print(scores[0], scores[-1])
#print(numpy.mean(scores))
        
        
            
            
            
            
            
            