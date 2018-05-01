import numpy as np
import pickle
import gensim
import random
import re

random.seed(0)

EMBEDDINGS_FILE = "/home/adam/project-adamrehan/src/embeddings/algebra_embeddings"#"/home/adam/project-adamrehan/src/embeddings/GoogleNews-vectors-negative300.bin.gz"
#CONSTRUCT_EMBEDDINGS_FILE = "/home/adam/project-adamrehan/src/scripts/construct.npy"
#DESTROY_EMBEDDINGS_FILE = "/home/adam/project-adamrehan/src/scripts/destroy.npy"
CONSTRUCT_MATRIX_FILE = "/home/adam/project-adamrehan/src/embeddings/construct_matrix.npy"
DESTROY_MATRIX_FILE = "/home/adam/project-adamrehan/src/embeddings/destroy_matrix.npy"

VERBSLIST1 = "./verbs_list1"
VERBSLIST2 = "./verbs_list2"

OBSERVATION = 'observation'
CONS = 'construct'
DESTROY = 'destroy'
NTRANS = 'n_transfer'
PTRANS = 'p_transfer'
GET = 'get'

class VerbClassifier():
    def __init__(self):
        # A matrix 
        #self.W = self.loadWordEmbeds(EMBEDDINGS_FILE)
        self.labeled_verbs = self._get_labeled_verbs_dict()
        #self.construct_embed = self.loadLabelEmbeds(CONSTRUCT_EMBEDDINGS_FILE)
        #self.destroy_embed = self.loadLabelEmbeds(DESTROY_EMBEDDINGS_FILE)
        self.construct_matrix = self.loadLabelEmbeds(CONSTRUCT_MATRIX_FILE)
        self.destroy_matrix = self.loadLabelEmbeds(DESTROY_MATRIX_FILE)

    def _get_labeled_verbs_dict(self):
        lines = [l.strip() for l in open(VERBSLIST1)]
        lines += [l.strip() for l in open(VERBSLIST2)]

        d = []
        c = []
        for line in lines:
            tup = [w.strip() for w in re.sub('\t',' ', line).split(' ')]
            if len(tup) == 2 and tup[1] == "d":
                d.append(tup[0])
            elif len(tup) == 2 and tup[1] == "c":
                c.append(tup[0])

        random.shuffle(d)
        random.shuffle(c)
        return {"d": d, "c": c}
                
    def get_average_embedding(self, words):
        embeds = self.W[words]
        # n x DIMS -> DIMS of average
        return np.average(embeds, axis=0)

    def get_label_embeds(self, label):
        if label in [CONS, PTRANS]:
            return self.construct_matrix
        elif label in [DESTROY, NTRANS]:
            return self.destroy_matrix
        else:
            raise Exception("Unexpected label %s" % label)
        
    def get_label_annotations(self, label):
        if label in [CONS, PTRANS]:
            return "c"
            #return self.construct_matrix
        elif label in [DESTROY, NTRANS]:
            return "d"
            #return self.destroy_matrix
        else:
            raise Exception("Unexpected label %s" % label)
        
    def classify(self, labels, verb):
        """
        labels: the constrained set of possible labels
        verb_phrase: a list of the verb and its arguments

        return: a list of the labels ordered by how likely each is

        Because labels are always scoped such that we only have to choose
        between construct/destroy, and negatie/positive transfer
        We basically just need to decide if we have an instance of
        the Agent of the verb gaining or losing something
        """
        #embed = self.get_average_embedding(verb_phrase)
        #similarity_dict = {l: 0.0 for l in labels}
        #for l in labels:
        #    similarity_dict[l] = self._get_max_similarity(embed, l)

        # Return labels in order of how similar their embedding is to
        # the input verb phrase
        #return sorted(similarity_dict, key=similarity_dict.get, reverse=True)
        if verb in self.labeled_verbs["d"]:
            return NTRANS if NTRANS in labels else DESTROY
        elif verb in self.labeled_verbs["c"]:
            return PTRANS if PTRANS in labels else CONS
    
    def _get_max_similarity(self, embed, l):
        sims = []
        for class_embedding in self.get_label_embeds(l):
            sims.append(self._cosine_sim(embed, class_embedding))
        #print(sims)
        #for verb in self.labeled_verbs[self.get_label_embeds(l)]:
        #    sims.append(self._cosine_sim(embed, self.W[verb]))

        #print(self.labeled_verbs[self.get_label_embeds(l)])
        #print(sims)
        return max(sims)

    def _cosine_sim(self, w1, w2):
        """
        Get the cosine similarity between 2 n-dimensional vectors

        dot-product / product of norms
        """
        return np.dot(w1, w2) / (np.linalg.norm(w1) * np.linalg.norm(w2))
        
    def loadWordEmbeds(self, filename):
        #return gensim.models.KeyedVectors.load(filename)
        return gensim.models.KeyedVectors.load_word2vec_format(\
                                    filename, binary=True)
        
    def loadLabelEmbeds(self, filename):
        """
        Load the embeddings trained for each Label
        """
        return np.load(filename)

if __name__=='__main__':
    vc = VerbClassifier()
    labels = [CONS, DESTROY]
    verb = "eats"
    print(vc.classify(labels, verb))
    
    
