import numpy as np
import pickle
import gensim

EMBEDDINGS_FILE ="/home/adam/project-adamrehan/src/embeddings/GoogleNews-vectors-negative300.bin.gz"
CONSTRUCT_EMBEDDINGS_FILE = "/home/adam/project-adamrehan/src/embeddings/construct_embedding.npy"
DESTROY_EMBEDDINGS_FILE = "/home/adam/project-adamrehan/src/embeddings/destroy_embedding.npy"

OBSERVATION = 'observation'
CONS = 'construct'
DESTROY = 'destroy'
NTRANS = 'n_transfer'
PTRANS = 'p_transfer'
GET = 'get'

class VerbClassifier():
    def __init__(self):
        # A matrix 
        self.W = self.loadWordEmbeds(EMBEDDINGS_FILE)
        self.construct_embed = self.loadLabelEmbeds(CONSTRUCT_EMBEDDINGS_FILE)
        self.destroy_embed = self.loadLabelEmbeds(DESTROY_EMBEDDINGS_FILE)
        
    def get_average_embedding(self, words):
        embeds = self.W[words]
        # n x DIMS -> DIMS of average
        return np.average(embeds, axis=0)

    def get_label_embeds(self, label):
        if label in [CONS, PTRANS]:
            return self.construct_embed
        elif label in [DESTROY, NTRANS]:
            return self.destroy_embed
        else:
            raise Exception("Unexpected labe %s" % label)
        
    def classify(self, labels, verb_phrase):
        """
        labels: the constrained set of possible labels
        verb_phrase: a list of the verb and its arguments

        return: a list of the labels ordered by how likely each is

        Because labels are always scoped such that we only have to choose
        between construct/destroy, and negatie/positive transfer
        We basically just need to decide if we have an instance of
        the Agent of the verb gaining or losing something
        """
        embed = self.get_average_embedding(verb_phrase)
        similarity_dict = {l: 0.0 for l in labels}
        for l in labels:
            similarity_dict[l] = self._cosine_sim(embed,\
                                        self.get_label_embeds(l))

        # Return labels in order of how similar their embedding is to
        # the input verb phrase
        return sorted(similarity_dict, key=similarity_dict.get, reverse=True)

    def _cosine_sim(self, w1, w2):
        """
        Get the cosine similarity between 2 n-dimensional vectors

        dot-product / product of norms
        """
        return np.dot(w1, w2) / (np.linalg.norm(w1) * np.linalg.norm(w2))
        
    def loadWordEmbeds(self, filename):
        return gensim.models.KeyedVectors.load_word2vec_format(\
                                    filename, binary=True)

    def loadLabelEmbeds(self, filename):
        """
        Load the embeddings trained for each Label
        """
        return np.load(filename)
