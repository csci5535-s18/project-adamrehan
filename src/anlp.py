import spacy

class AlgebraNLP(object):
    def __init__(self):
        self.nlp = spacy.load('en')
    def dependency_parse(self, sentence):
        pass
    def get_command_tuple(self, sentence):
        pass