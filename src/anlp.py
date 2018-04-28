import spacy
from word2number import w2n

class AlgebraNLP(object):
    def __init__(self):
        self.nlp = spacy.load('en')
        self.variables_list = []
        
    def get_observation_arguments(self, sentence):
        """
        We assume a sentence is a single meaningful chunk of text,
        with coreference resolution already done in preprocessing 
        """
        tokens = self.nlp(sentence)
        quantifier = self._get_quantifier(tokens)
        V = self._get_parent_verb(quantifier)
        nobject_string = self._get_nobject_string(V)
        nsubject_string = self._get_nsubject_string(V)

        print(nobject_string, nsubject_string)
        
        #w2n.word_to_num(quantifier.text)

    def reset_variables_list(self):
        self.variables_list = []

    def _get_nobject_string(self, V):
        """
        Get the string that represents the part of the variable name
        correspodning to the object of the verb.

        modifier_deps will tell the _get_deps_strings method
        which dependents to append to the string
        """
        modifier_deps = ["amod", "nmod"]
        # For holding the strings that modify the dobj
        mods = []
        for c in V.children:
            if c.dep_ in ["dobj"]:
                dobj = c
                mods += self._get_deps_strings(dobj,\
                                                [], modifier_deps)
        return "_".join([dobj.text] + mods)

    def _get_nsubject_string(self, V):
        """                                                                                                                                           
        Get the string that represents the part of the variable name                                                                                  
        correspodning to the subject of the verb.                                                                                                     
                                                                                                                                                      
        modifier_deps will tell the _get_deps_strings method                                                                                          
        which dependents to append to the string                                                                                                      
        """
        modifier_deps = ["amod", "nmod", "poss"]
        # For holding the strings that modify the dobj
        mods = []
        for c in V.children:
            if c.dep_ in ["nsubj"]:
                nsubj = c
                mods += self._get_deps_strings(nsubj,\
                                                [], modifier_deps)
        return "_".join([nsubj.text] + mods)
        
    def _get_quantifier(self, tokens):
        """
        We assume each sentence has exactly one quantifier
        """
        for token in tokens:
            if self._is_quantifier(token):
                return token

    def _is_quantifier(self, token):
        return token.like_num
        
    def _get_parent_verb(self, token):
        """
        Get the first parent of some token
        that is a verb
        """
        def _get_parent_verb_rec(t):
            if t.head.pos_ == "VERB":
                return t.head
            else:
                return _get_parent_verb_rec(t.head)

        return _get_parent_verb_rec(token)
        
    def _get_deps_strings(self, token, deps_list=[], constraints=[]):
        for c in token.children:
            if c.dep_ in constraints:
                deps_list.append(c.text)
                self._get_deps_strings(c, deps_list, constraints)

        return deps_list

if __name__=='__main__':
    # Test _get_deps_strings
    x = AlgebraNLP()
    s = u"Pooja's Mom has 3 delicious green apples"

    print(x.get_observation_arguments(s))
