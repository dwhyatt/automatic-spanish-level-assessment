# -*- coding: UTF-8- -*-
#!/bin/env python3.4

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