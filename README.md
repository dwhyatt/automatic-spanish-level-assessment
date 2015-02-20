Ongoing work to automatically evaluate native English speaking learners of Spanish.


The data for this project comes from the SPLLOC project:

http://www.splloc.soton.ac.uk

The data used is from three narrative tasks from SPLLOC - the Loch Ness Narrative from SPLLOC 1, and the Nati y Pancho Narrative and the Hermanas Narrative from SPLLOC 2.  These were chosen because they weren't developed to draw out any particular feature of learner language (such as ser and estar use), and as they presumably evoke relatively comparable content, unlike tasks which ask for participants to describe different famous people or to talk about things in their own life.  The participants in each subcorpora consisted of three groups of learners and a control group of native speakers. The three levels of learner groups are described in the corpus as corresponding to the three macro levels of the Common European Framework (CEF) reference for evaluating L2 ability. 

To get Mate Tools (including Spanish models):

https://code.google.com/p/mate-tools/downloads/list


To download Freeling, an excellent Spanish toolkit:

http://nlp.lsi.upc.edu/freeling/


To download ParaMorpho, a morphological analyzer for Spanish (and Guarani!):

http://www.cs.indiana.edu/~gasser/Research/software.html


And NLTK for python3:

http://www.nltk.org/install.html


In brief, this code uses a combination of brute-force methods (such as POS-tag trigrams) and linguistically-motivated features (such as percentage of null subjects and agreement errors) to identify the level of Spanish learners.  Mate dependency parses and Freeling constituency parses are both used.  ParaMorfo is used to analyze verb forms, which are the big morphological challenge in Spanish (and morphology is always a big problem for L2 learners!).  The resulting feature-set is used to build a model for scikit's SVM tool.

The files 'consituency_features.py', 'dependency_features.py', and 'vector_features.py' have the classes with the methods which get (numerical) data from the (text) data for the feature set.  'test_features.py' and 'run_svm.py' import and call these classes, with the difference being that 'test_features.py' is mainly to be run to produce descriptive statistics for the four CEF classes (basically beginner, intermediate, advanced, native) to get a sense of how the features perform, while 'run-svm.py' throws the feature set into the black box of scikit's SVM implementation and then tests performance on held-out data.


