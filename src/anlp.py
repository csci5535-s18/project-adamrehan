import spacy
from word2number import w2n

class AlgebraNLP(object):
    def __init__(self):
        self.nlp = spacy.load('en')
        
        
    def get_observation_tuple(self, sentence):
        """
        We assume a sentence is a single meaningful chunk of text,
        with coreference resolution already done in preprocessing 
        """
        tokens = nlp(sentence)
        quantifier = self._get_quantifier(tokens)
        V = self._get_parent_verb(quantifier)
        nobject_string = self._get_object_string(V)
        #nsubject_string =
        
        w2n.word_to_num(quantifier.text)

    #def _get_object_string(self, V):
    #    for c in V.children:
    #        if c.dep_ in ["dobj"]:
                
        
    def _get_quantifier(self, tokens):
        """
        We assume each sentence has exactly one quantifier
        """
        for token in tokens:
            if _is_quantifier(token):
                return token

    def _is_quantifier(self, token):
        return token.text.like_num
        
    def _get_parent_verb(self, token):
        """
        Get the first parent of some token
        that is a verb
        """
        def _get_parent_verb_rec(t):
            if t.head.pos == "VERB":
                return t.head
            else:
                return _get_parent_verb_rec(t.head)

        return _get_parent_verb_rec(token)
        
    def _get_deps_strings(self, token, deps_list=[], constraints=[]):
        for c in token.children:
            print(c.dep_)
            if c.dep_ in constraints:
                deps_list.append(c.text)
                self._get_deps_strings(c, deps_list, constraints)

        return deps_list

if __name__=='__main__':
    # Test _get_deps_strings
    x = AlgebraNLP()
    tokens = x.nlp(u"has 3 green apples")
    print(x._get_deps_strings(tokens[0], [], "dobj, amod"))
