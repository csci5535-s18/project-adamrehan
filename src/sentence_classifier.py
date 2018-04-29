import numpy as np
import pickle

OBSERVATION = 'observation'
CONS = 'construct'
DESTROY = 'destroy'
NTRANS = 'n_transfer'
PTRANS = 'p_transfer'
GET = 'get'

class VerbCategoryClassifier(object):
    def __init__(self, classnames=None, verbs=None):
        # self.classnames = classnames
        # self.n_components = len(classnames)
        self.verbs = verbs
    def vectorize(self, sentences):
        '''
        getting features out of sentences: using Wordnet, word2vec, Verbnet, etc
        If self.verbs is None: We'll need to extract the verbs
        :param sentences:
        :return:
        '''
        pass
    def extract_verbs(self, sentences):
        pass
    def fit(self, X, y):
        pass
    def predict(self, X):
        pass
    def predict_labels(self, sentences):
        # Todo:
        return [OBSERVATION, DESTROY, GET]
    def fit_predict(self, X):
        pass
def load(filename):
    # TODO:
    return VerbCategoryClassifier()
    # return VerbCategoryClassifier(pickle.load(open(filename, 'rb')))
