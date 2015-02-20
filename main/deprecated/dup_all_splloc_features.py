# -*- coding: UTF-8- -*-
#!/bin/env python3.4

import os
import sys
import l3  #http://www.cs.indiana.edu/~gasser/Research/software.html
from io import StringIO
from nltk import *


class LemmaFeatures:

    def __init__(self, rootdir): 
        self.rootdir = rootdir
        self.lemma_list = self.makeLemmaList()
        


    def makeLemmaList(self):  ### this should only be called once at top of document

        lem_list = []

        for subdir, dirs, files in os.walk(self.rootdir):
            
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


class WordFeatures:

    def __init__(self, text):
        self.text = text
        self.sentences = self.getSentences()
        self.stem_dict = {}
        self.tam_dict = {'presente': [], 'gerundio': [], 'preterito': [], 'imperfecto': [], 'subjuntivo_presente': [], 'subjuntivo_imperfeto': [], 'futuro': [],
        'infinitivo': [], 'participio': [], 'imperativo': []}

        self.subj_dict = {'1s': 0, '2s': 0, '3s': 0, '1p': 0, '2p': 0, '3p': 0}

        self.getVerbFeatures()


    def getSentences(self):
        all_conll_sentences = []
        # all_words_sentences = []

        conll_sentence = []
        # words_sentence = []

        for line in self.text:
            line = line.strip()
            
            if line:
                line = line.split('\t')
                if line[0] == '1':
                    
                    conll_sentence.append(line)
                    # words_sentence.append(line[1])

                else:
                    
                    conll_sentence.append(line)
                    # words_sentence.append(line[1])
            else:
                
                all_conll_sentences.append(conll_sentence)
                # all_words_sentences.append(words_sentence)

                conll_sentence = []
                # words_sentence = []

        return all_conll_sentences
            

    def findAgreementErrors(self):
        sentences = self.sentences 

        ### deceptive gender words do not include words (such as cometa, atleta, radio, etc.) which may be either gender
        ### List taken from http://en.wiktionary.org/wiki/Category:Spanish_nouns_with_irregular_gender and http://www.spanishdict.com/topics/show/1
        ### These lists are cases in which the gender goes against the most common gender for the final vowel or coda, and thus seem likely candidates for user errors in agreement.
        ### for now, nouns ending in consonants are not considered except for a few exceptional classes

        masculine_exceptions = ['anagrama', 'aroma', 'axioma', 'califa', 'carisma', 'clima', 'cólera', 'día', 'diagrama', 'dilema', 'diploma', 'drama', 'emblema'
        'enigma', 'esquema','fantasma', 'gorila', 'idioma', 'karma', 'mapa', 'morfema', 'nirvana', 'panorama', 'pijama', 'piyama', 'planeta', 'plasma', 'poema'
        'problema', 'programa', 'sistema', 'sofá', 'síntoma', 'telegrama', 'tema', 'teorema', 'tranvía']

        feminine_end_in_o = ['foto', 'mano', 'moto']

        feminine_end_in_e = ['calle', 'carne', 'clase', 'clave', 'corriente', 'fe', 'frase', 'fuente', 'gente', 'leche', 'lente', 'mente', 'muerte', 'nieve', 
        'noche', 'nube', 'sangre', 'sede', 'serpiente', 'tarde', 'suerte', 'tarde', 'torre'] 

        feminine_exceptions = feminine_end_in_e + feminine_end_in_o

        
        dep_pairs = []
        for sent in self.sentences:
            
            for line in sent:

                word_id = line[0]
                word = line[1]
                lemma = line[3]
                tag = line[5]
                dep = line[9]

                if tag == 'n':
                    if word[0].isupper():
                        pass
                    else:
                        for l in sent:
                            if l[9] == word_id:
                                if l[5] == 'd' or l[5] == 'a':
                                    dep_pairs.append(((l[1]).lower(), lemma))
       
        agree = 0
        error = 0
        number_masculine = 0
        number_feminine = 0

        for pair in dep_pairs:
            noun = pair[1]
            mod = pair[0]
            #print(mod, noun)
            
            if noun in masculine_exceptions:
                noun = 'M'
            elif noun in feminine_exceptions:
                noun = 'F'
            elif noun.endswith('ión') or noun.endswith('dad'):
                noun = 'F'
            elif noun.endswith('o'):
                noun = 'M'
            elif noun.endswith('a'):
                noun = 'F'
            else:
                noun = 'U'

            if noun == 'M':
                number_masculine += 1
            elif noun == 'F':
                number_feminine += 1
            
            if mod.endswith('o'):
                mod = 'M'
            elif mod.endswith('a'):
                mod = 'F'
            elif mod[:-1].endswith('o'):
                mod = 'M'
            elif mod[:-1].endswith('a'):
                mod = 'F'
            elif mod == 'un' or mod == 'el':
                mod = 'M'
            elif mod == 'buen' or mod == 'aquel':
                mod = 'M'
            else:
                mod = 'U'
            
            if mod == 'U' or noun == 'U':
                pass

            else:
                
                if mod == noun:
                    agree += 1
                else:
                    error += 1



        percentage_agree = agree/(agree + error)

        if number_masculine == 0:
            masc_fem_ratio = 0
        else:
            masc_fem_ratio = number_feminine/number_masculine


        return [percentage_agree, masc_fem_ratio]

    def basicCountFeatures(self):

        sent_lengths = []
        word_length = []
        type_token = []

        for sent in self.sentences:
            sent_lengths.append(len(sent))
            for line in sent:
                word = line[1]
                lemma = line[3]
                word_length.append(len(word))
                type_token.append(lemma)

        average_len_sentence = sum(sent_lengths)/len(sent_lengths)
        average_len_word = sum(word_length)/len(word_length)
        type_token = len(set(type_token))/len(type_token)

        return [average_len_sentence, average_len_word, type_token]

   
    def getVerbFeatures(self):
        
        stem_dict = self.stem_dict
        tam_dict = self.tam_dict
        subj_dict = self.subj_dict

        

        paramorph = []
        for sentence in self.sentences:
            for line in sentence:
                
                word = line[1]
                tag = line[5]
                if tag == 'v':
                    with Capturing() as output:
                        l3.anal('es', word)
                    paramorph.append(output)
                    
        
        for p in paramorph:
            p = list(p)
            
            if 'Cargando datos' in p[0]:
                p.remove(p[0])
            
            palabra = p[0].split(':')[1].strip()

            if p[0].startswith('?'):
                raiz = 'Undefined'
            if p[1]:  
                
                raiz = p[1].split('=')[1].strip().rstrip('>').lstrip('<')
            else:
                raiz = 'Undefined'
            

            if len(p) >  4:

                i = 0
                time = False; subject = False

                while i < len(p):
                    if time == True and subject == True:
                        break
                    if time == False:
                        if 'tiempo/aspecto/modo' in p[i]:
                            tam = p[i].split('=')[1].strip()
                            time = True
                    if subject == False:
                        if 'sujeto' in p[i]:
                            sujeto = p[i].split('=')[1].strip()
                            subject = True
                    i += 1
                if time == False:
                    tam = 'Undefined'
                if subject == False:
                    sujeto = 'Undefined'

            else:

                tam = 'Undefined'; sujeto = 'Undefined'

           
            #print('palabra:', palabra, 'raiz:', raiz, 'tam:', tam, 'sujeto:', sujeto)
            
            if raiz not in stem_dict:
                stem_dict[raiz] = [palabra]
            else:
                stem_dict[raiz].append(palabra)

            
            if tam.startswith('imperfecto'):
                tam_dict['imperfecto'].append(palabra)

            elif tam.startswith('infinitivo'):
                tam_dict['infinitivo'].append(palabra)

            elif tam.startswith('pretérito') or tam.startswith('+pretérito'):
                tam_dict['preterito'].append(palabra)

            elif tam.startswith('presente'):
                tam_dict['presente'].append(palabra)

            elif tam.startswith('gerundio'):
                tam_dict['gerundio'].append(palabra)

            elif tam.startswith('participio'):
                tam_dict['participio'].append(palabra)

            elif tam.startswith('futuro'):
                tam_dict['futuro'].append(palabra)

            elif tam.startswith('subjuntivo imperfecto'):
                tam_dict['subjuntivo_imperfeto'].append(palabra)

            elif tam.startswith('subjuntivo presente'):
                tam_dict['subjuntivo_presente'].append(palabra)

            elif tam.startswith('imperativo'):
                tam_dict['imperativo'].append(palabra)
            else:
                pass

            if sujeto == 'Undefined':
                pass

            elif sujeto == '2/3 persona plural':
                subj_dict['2p'] += 1
                subj_dict['3p'] += 1

            elif sujeto == '1/3 persona singular':
                subj_dict['1s'] += 1
                subj_dict['3s'] += 1

            elif sujeto == '3 persona singular':
                subj_dict['3s'] += 1

            elif sujeto == '1 persona singular':
                subj_dict['1s'] += 1

            elif sujeto == '2 persona singular':
                subj_dict['2s'] += 1

            elif sujeto == '1 persona plural':
                subj_dict['1s'] += 1

            else:
                print('misssed this one ', sujeto)


        # for k,v in stem_dict.items():
        #     print(k,v)
        # print('\n')
        # for k,v in tam_dict.items():
        #     print(k,v)
        # print('\n')
        # for k,v in subj_dict.items():
        #     print(k,v)
        

    def serEstar(self):
        stem_dict = self.stem_dict

        if 'ser' in stem_dict:
            ser = stem_dict['ser']
            s_all = len(ser)
            ser_forms = len(set(ser))
        else:
            ser = None
            s_all = 0
            ser_forms = 0

        if 'era' in stem_dict:
            era = stem_dict['era']
            er_all = len(era)
            era_forms = len(set(era))
        else:
            era = None
            er_all = 0
            era_forms = 0

        if 'estar' in stem_dict:
            estar = (stem_dict['estar'])
            es_all = len(estar)
            estar_forms = len(set(estar))
        else:
            estar = None
            es_all = 0
            estar_forms = 0

        if era is not None:
            ser_forms = ser_forms + era_forms
            s_all = s_all + er_all

        if es_all != 0:
            ser_estar_ratio = s_all/es_all
        else:
            ser_estar_ratio = 0
        

        
        if s_all != 0:
            ser_type_token = ser_forms/s_all
        else:
            ser_type_token = 0

        if es_all != 0:
            estar_type_token = estar_forms/es_all
        else:
            estar_type_token = 0

        return [ser_estar_ratio, ser_type_token, estar_type_token]

    def getCompoundTenses(self):

        perifrastic_future = []
        perfect_verbs = []
        progressive_verbs = []

        for sent in self.sentences:
            
            for line in sent:

                word_id = line[0]
                word = line[1]
                lemma = line[3]
                tag = line[5]
                dep = line[9]

                if tag == 'v':

                    if lemma == 'ir':
                        for l in sent:
                            if l[0] == dep:
                                if l[5] == 'v':
                                    if l[1].endswith('r'):
                                        perifrastic_future.append((word, (l[1]).lower()))
                    if lemma == 'haber':
                        for l in sent:
                            if l[0] == dep:
                                if l[5] == 'v':
                                    if l[1].endswith('do'):
                                        perfect_verbs.append((word, (l[1]).lower()))
                    if lemma == 'estar':
                        for l in sent:
                            if l[0] == dep:
                                if l[5] == 'v':
                                    if l[1].endswith('do'):
                                        progressive_verbs.append((word, (l[1].lower())))

        print(perifrastic_future)
        print(perfect_verbs)
        print(progressive_verbs)

        return [len(perifrastic_future), len(perfect_verbs), len(progressive_verbs)]
        

    def getVerbBasics(self):

        to_return = []

        for v in self.subj_dict.values():
            to_return.append(v)

        verb_types = len(self.stem_dict())
        verb_tokens = 0

        for v in self.stem_dict.values():
            t = len(v)
            verb_tokens += t

        for t in self.tam_dict.values():
            to_return.append(t)

        to_return.append(verb_types/verb_tokens)

        return [to_return]

    def getClitics(self):

        list_of_clitics = ['se', 'la', 'lo', 'le', 'los', 'las', 'les']
        clitics = []

        for sent in self.sentences:
            
            for line in sent:

                word_id = line[0]
                word = line[1]
                lemma = line[3]
                tag = line[5]
                dep = line[9]

                if tag == 'p':
                    if word in list_of_clitics:
                        clitics.append(word)

                elif tag == 'v':
                    for clitic in list_of_clitics:
                        if word.endswith(clitic):
                            clitics.append(word)

        return [len(clitics)]

    def getNullSubjets(self):  ### still very crude

        movement = open('freeling_data_files/spanish_movement_verbs.txt', 'r').readlines()
        a_verbs = open('freeling_data_files/spanish_a_verbs.txt', 'r').readlines()
        impersonals = open('freeling_data_files/spanish_movement_verbs.txt', 'r').readlines()
        transitives = open('freeling_data_files/spanish_transitive_verbs.txt', 'r').readlines() 
        intransitives = open('freeling_data_files/spanish_intransitive_verbs.txt', 'r').readlines()
        ditransitives = open('freeling_data_files/spanish_ditransitive_verbs.txt', 'r').readlines() 

        intransitives = [i.strip() for i in intransitives if i.strip()]
        ditransitives = [i.strip() for i in ditransitives if i.strip()]
        impersonals = [i.strip() for i in impersonals if i.strip()]
        movement = [i.strip() for i in movement if i.strip()]
        transitives = [i.strip() for i in transitives if i.strip()]
        a_verbs = [i.strip() for i in a_verbs if i.strip()]


        doubling_clitics = ['le', 'les', 'se']
        verbs_and_arguments = []

        for sent in self.sentences:
            this_sentence_verbs_and_arguments = []
            for line in sent:

                word_id = line[0]
                word = line[1]
                lemma = line[3]
                tag = line[5]
                dep = line[9]

                if tag == 'v':

                    verb = lemma
                    num_of_arguments = 0
                    if verb == 'haber' or word.endswith('r'):
                        pass
                    elif word.endswith('do') or word.endswith('se'):
                        pass

                    
                    else:
                        
                        for l1 in sent:
                            if l1[9] == word_id:
                                if l1[5] == 'n' or l1[5] == 'p':
                                    if l1[1] not in doubling_clitics:
                                        num_of_arguments += 1

                        for l2 in sent:
                            if l2[0] == word_id:
                                if l2[0] == 'a':
                                    if verb not in a_verbs:
                                        if verb not in movement:
                                            for l3 in sent:
                                                if l3[9] == l2[0]:
                                                    if l3[5] == 'n' or l3[5] == 'p':
                                                        if l1[1] not in doubling_clitics:
                                                            num_of_arguments += 1
                        
                    
                    #
                    this_sentence_verbs_and_arguments.append((verb, num_of_arguments))
            verbs_and_arguments.append(this_sentence_verbs_and_arguments)
            


        null = 0
        not_null = 0
        for sentence in verbs_and_arguments:
            for pair in sentence:

                verb = pair[0]
                arguments = pair[1]

                if arguments == 0:
                    if verb not in impersonals:
                        null += 1
                elif arguments == 1:
                    if verb in intransitives:
                        not_null += 1
                    elif verb in transitives:
                        null += 1
                elif arguments == 2:
                    if verb not in ditransitives:
                        not_null += 1
                else:
                    not_null += 1

        
        percentage_pro_drop = null/(null+not_null)
        
        return [percentage_pro_drop]



class Embeddings:

    def __init__(self, freeling):
        self.freeling = freeling

    def countEmbeddings(self):
        sentences = 0
        subord = 0

        for line in self.freeling:
            for word in line:
                if 'subord' in word:
                    subord += 1
                elif 'S_[' in word:
                    sentences += 1

        if sentences == 0:
            return 0

        else:
            return subord/sentences

    def getCoordinations(self):
        coordinating = 0
        subordinating = 0

        for line in self.freeling:
            if 'conj-subord_[' in line:
                subordinating += 1
            elif 'coord_[' in line:
                coordinating += 1

        if coordinating != 0:
            ratio = subordinating/coordinating
        else:
            ratio = 0

        return ratio


class Capturing(list):

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout


if  __name__ =='__main__': 

    text = open('/Users/danielwhyatt/Desktop/for_github/SPLLOC/Current/current_folder/splloc2CatNativexml/C32NTV13N.text_only.txt.conll.lemmas.coursetags.dependencies.txt', 'r').readlines()
    
    testing = WordFeatures(text) ### instantiate

   
    # testing.getVerbFeatures() ### this has to be called first

    print(testing.findAgreementErrors())
    # print(testing.getCompoundVerbs())
    # print(testing.serEstar())
    # print(testing.basicCountFeatures())
    print(testing.getClitics())

    print(testing.getNullSubjets())


    # directory = sys.argv[1]

    # lemmas = lemmaFeatures(directory)
    # all_lemmas = lemmas.makeLemmaList()
    # print(all_lemmas)



