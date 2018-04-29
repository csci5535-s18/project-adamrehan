import spacy
from word2number import w2n
import sentence_classifier as sc

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
        nsubject_string = self._get_nsubject_string(V)        
        nobject_string = self._get_nobject_string(V)
        # Store quantifier as an integer
        q_int = w2n.word_to_num(str(quantifier.text))
        variable_name = nsubject_string + "_" + nobject_string
        
        self.add_to_variables_list(variable_name)

        return [variable_name, q_int]

    def get_construct_arguments(self, sentence):
        """ 
        We assume a sentence is a single meaningful chunk of text,        
        with coreference resolution already done in preprocessing
        """
        tokens = self.nlp(sentence)
        quantifier = self._get_quantifier(tokens)
        V = self._get_parent_verb(quantifier)
        nsubject_string = self._get_nsubject_string(V)
        nobject_string = self._get_nobject_string(V)
        # Store quantifier as an integer
        q_int = w2n.word_to_num(str(quantifier.text))
        variable_name = nsubject_string + "_" + nobject_string

        self.add_to_variables_list(variable_name)

        return [variable_name, q_int]

    def get_destroy_arguments(self, sentence):
        """
        We assume a sentence is a single meaningful chunk of text,
        with coreference resolution already done in preprocessing
        """
        tokens = self.nlp(sentence)
        quantifier = self._get_quantifier(tokens)
        V = self._get_parent_verb(quantifier)
        nsubject_string = self._get_nsubject_string(V)
        nobject_string = self._get_nobject_string(V)
        # Store quantifier as an integer
        q_int = w2n.word_to_num(str(quantifier.text))
        variable_name = nsubject_string + "_" + nobject_string

        self.add_to_variables_list(variable_name)        
        
        return [variable_name, q_int]

    def get_negative_transfer_arguments(self, sentence):
        """
        We assume a sentence is a single meaningful chunk of text,      
        with coreference resolution already done in preprocessing

        negative transfer example: Pooja gives one apple to John
        """
        tokens = self.nlp(sentence)
        quantifier = self._get_quantifier(tokens)
        V = self._get_parent_verb(quantifier)
        nsubject_string = self._get_nsubject_string(V)
        nobject_string = self._get_nobject_string(V)
        # Store quantifier as an integer
        q_int = w2n.word_to_num(str(quantifier.text))
        variable_name = nsubject_string + "_" + nobject_string

        self.add_to_variables_list(variable_name)
        
        return [variable_name, q_int]

    def get_get_arguments(self, sentence):
        """
        We assume a sentence is a single meaningful chunk of text,
        with coreference resolution already done in preprocessing
        negative transfer example: Pooja gives one apple to John  
        """
        tokens = self.nlp(sentence)
        quantifier = self._get_quantifier(tokens)
        V = self._get_parent_verb(quantifier)
        nsubject_string = self._get_nsubject_string(V)
        nobject_string = self._get_nobject_string(V)
        # Store quantifier as an integer

        variable_name = nsubject_string + "_" + nobject_string

        self.add_to_variables_list(variable_name)
        
        return [variable_name]

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
        return "_".join([dobj.lemma_.lower()] + [m.lemma_.lower() for m in mods])

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
        return "_".join([nsubj.lemma_.lower()] + [m.lemma_.lower() for m in mods])
        
    def _get_quantifier(self, tokens):
        """
        We assume each sentence has exactly one quantifier
        """
        for token in tokens:
            if self._is_quantifier(token):
                return token

    def _is_quantifier(self, token):
        QUANTIFIER_STRINGS = ["some", "many", "few", "much", "several", "every", "all"]

        if token.text in QUANTIFIER_STRINGS:
            return True
        else:
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
            # Only return the strings that have deps in the constraints list
            # We also NEVER want to return the quantifier
            # Even when it serves as e.g. a modifier.
            if c.dep_ in constraints and not self._is_quantifier(c):
                deps_list.append(c.text)
                self._get_deps_strings(c, deps_list, constraints)

        return deps_list

    def get_commands(self, sentences, labels):
        commands = []
        self.variables_list = []
        for label, sentence in zip(labels, sentences):
            if label == sc.OBSERVATION:
                commands.append([sc.OBSERVATION] + self.get_observation_arguments(sentence))
            elif label == sc.DESTROY:
                commands.append([sc.DESTROY] + self.get_destroy_arguments(sentence))
            elif label == sc.GET:
                commands.append([sc.GET] + self.get_get_arguments(sentence))
        return commands

    def add_to_variables_list(self, variable):
        if variable not in self.variables_list:
            self.variables_list.append(variable)

if __name__=='__main__':
    # Test _get_deps_strings
    x = AlgebraNLP()
    s = u"How many apples does Pooja have now?"

    print(x.get_get_arguments(s))
