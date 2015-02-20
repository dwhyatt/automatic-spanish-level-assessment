Ongoing work to automatically evaluate native English speaking learners of Spanish.


The data for this project comes from the SPLLOC project:

http://www.splloc.soton.ac.uk

The Data used is from three narrative tasks from SPLLOC - the Loch Ness Narrative from SPLLOC 1, and the Nati y Pancho Narrative and the Hermanas Narrative from SPLLOC 2.  These are used as they were not developed to elicit any particular feature of learner language (such as ser and estar use), and as they presumably elicit relatively homogenous content, unlike tasks which ask for participants to describe different famous individuals, or tasks related to things in the participant’s own life.  The participants in each subcorpora consisted of three groups of learners and a control group of native speakers. The three levels of learner groups are described in the corpus as corresponding to the three macro levels of the Common European Framework reference for evaluating L2 ability. 

To get Mate Tools (including Spanish models):

https://code.google.com/p/mate-tools/downloads/list


To download Freeling, an excellent Spanish toolkit:

http://nlp.lsi.upc.edu/freeling/


To download ParaMorpho, a morphological analyzer for Spanish (and Guarani!):

http://www.cs.indiana.edu/~gasser/Research/software.html


In brief, this code uses a combination of brute-force methods (such as POS-tag trigrams) and linguistically-motivated features (such as percentage of null subjects and agreement erros) to identify the level of Spanish learners.  Mate dependency parses and Freeling constituency parses are both used.  ParaMorfo is used to analyze verb forms, which are the big morphological challenge in Spanish (and morphology is always a big problem for L2 learners).  The resulting feature-set is used to build a model for scikit's SVM tool, and then tested on held-out data.


