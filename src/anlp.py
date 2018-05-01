import spacy
from word2number import w2n
import sentence_classifier as sc
from stanfordcorenlp import StanfordCoreNLP
from spacy.tokens.token import Token

class AlgebraNLP(object):
    def __init__(self, use_stanford=False):
        self.nlp = spacy.load('en')
        if use_stanford:
            print 'creating core server'
            self.snlp = StanfordCoreNLP(r'http://localhost', port=9000)
            print 'done creating core server'
            print 'initializing dep parse'
            self.snlp.dependency_parse(u'test')
            print 'done initializing dep parse'
            self._use_stanford = True
        else:
            self._use_stanford = False
        self.variables_list = []
        self.verb_classifier = sc.VerbClassifier()

    def __del__(self):
        if self._use_stanford:
            self.snlp.close()

    def get_tokens(self, sentence):
        tokens = self.nlp(sentence)
        sentence = []
        
        for i, t in enumerate(tokens):
            if t.pos_ == "PROPN":
                if i == 0:
                    sentence.append("she")
                else:
                    sentence.append("me")
            else:
                sentence.append(t.text)
        sentence = ' '.join(sentence)
        if self._use_stanford:
            updated_tokens = []
            # print 'creating dep parse'
            stanford_parse = self.snlp.dependency_parse(sentence)
            # print 'done creating dep parse'
            for token in tokens:
                updated_tokens.append(token)
            for index, token in enumerate(updated_tokens):
                children = []
                for s_token in stanford_parse:
                    dep_name = s_token[0]
                    tok_ind = s_token[1] - 1
                    dep_index = s_token[2] - 1
                    if tok_ind == index:
                        tokens[dep_index].head = token
                        tokens[dep_index].dep_ = dep_name
                        children.append(tokens[dep_index])
                # token.children = children
                # updated_tokens.append(token)
            return updated_tokens
        return tokens


    def get_observation_arguments(self, tokens):
        """
        We assume a sentence is a single meaningful chunk of text,
        with coreference resolution already done in preprocessing 
        """
        # tokens = self.nlp(sentence)
        quantifier = self._get_quantifier(tokens)
        V = self._get_parent_verb(quantifier)
        nsubject_string = self._get_nsubject_string(V)        
        dobject_string = self._get_dobject_string(V)
        # Store quantifier as an integer
        q_int = w2n.word_to_num(str(quantifier.text))
        variable_name = nsubject_string + "_" + dobject_string
        
        self.add_to_variables_list(variable_name)

        return [variable_name, q_int]

    def get_construct_arguments(self, tokens):
        """ 
        We assume a sentence is a single meaningful chunk of text,        
        with coreference resolution already done in preprocessing
        """
        # tokens = self.nlp(sentence)
        quantifier = self._get_quantifier(tokens)
        V = self._get_parent_verb(quantifier)
        nsubject_string = self._get_nsubject_string(V)
        dobject_string = self._get_dobject_string(V)
        # Store quantifier as an integer
        q_int = w2n.word_to_num(str(quantifier.text))
        variable_name = nsubject_string + "_" + dobject_string

        self.add_to_variables_list(variable_name)

        return [variable_name, q_int]

    def get_destroy_arguments(self, tokens):
        """
        We assume a sentence is a single meaningful chunk of text,
        with coreference resolution already done in preprocessing
        """
        # tokens = self.nlp(sentence)
        quantifier = self._get_quantifier(tokens)
        V = self._get_parent_verb(quantifier)
        nsubject_string = self._get_nsubject_string(V)
        dobject_string = self._get_dobject_string(V)
        # Store quantifier as an integer
        q_int = w2n.word_to_num(str(quantifier.text))
        variable_name = nsubject_string + "_" + dobject_string

        self.add_to_variables_list(variable_name)        
        
        return [variable_name, q_int]

    def get_negative_transfer_arguments(self, tokens):
        """
        We assume a sentence is a single meaningful chunk of text,      
        with coreference resolution already done in preprocessing

        negative transfer example: Pooja gives one apple to John
        """
        # tokens = self.nlp(sentence)
        quantifier = self._get_quantifier(tokens)
        V = self._get_parent_verb(quantifier)
        nsubject_string = self._get_nsubject_string(V)
        dobject_string = self._get_dobject_string(V)
        iobject_string = self._get_iobject_string(V)
        
        # Store quantifier as an integer
        q_int = w2n.word_to_num(str(quantifier.text))
        variable_names = [nsubject_string + "_" + dobject_string, iobject_string + "_" + dobject_string]

        for variable_name in variable_names:
            self.add_to_variables_list(variable_name)
        
        return [variable_names[0], variable_names[1], q_int]

    def get_positive_transfer_arguments(self, tokens):
        """                                                                                                                                           
        We assume a sentence is a single meaningful chunk of text,                                                                                    
        with coreference resolution already done in preprocessing     
        positive transfer example: Pooja takes one apple from John
        """
        quantifier = self._get_quantifier(tokens)
        V = self._get_parent_verb(quantifier)
        nsubject_string = self._get_nsubject_string(V)
        dobject_string = self._get_dobject_string(V)
        iobject_string = self._get_iobject_string(V)

        # Store quantifier as an integer
        q_int = w2n.word_to_num(str(quantifier.text))
        variable_names = [nsubject_string + "_" + dobject_string, iobject_string + "_" + dobject_string]

        for variable_name in variable_names:
            self.add_to_variables_list(variable_name)

        return [variable_names[0], variable_names[1], q_int]

    def get_get_arguments(self, tokens):
        """
        We assume a sentence is a single meaningful chunk of text,
        with coreference resolution already done in preprocessing
        negative transfer example: Pooja gives one apple to John  
        """
        # tokens = self.nlp(sentence)
        quantifier = self._get_quantifier(tokens)
        V = self._get_parent_verb(quantifier)
        nsubject_string = self._get_nsubject_string(V)
        dobject_string = self._get_dobject_string(V)

        variable_name = nsubject_string + "_" + dobject_string

        # self.add_to_variables_list(variable_name)
        
        return [variable_name]

    def classify_and_get_sentences(self, sentences):
        commands = []
        self.reset_variables_list()
        for sentence in sentences:
            tokens = self.get_tokens(sentence)
            label = self.classify(tokens)
            commands.append(self.get_commands([sentence], [label])[0])
            # co.append(self.classify(tokens))
        return commands

    def classify(self, tokens):
        quantifier = self._get_quantifier(tokens)
        V = self._get_parent_verb(quantifier)
        nsubject_string = self._get_nsubject_string(V)
        dobject_string = self._get_dobject_string(V)
        variable_name = '{}_{}'.format(nsubject_string, dobject_string)

        if "?" in [t.text for t in tokens]:
            return sc.GET
        if variable_name in self.variables_list:
            #If there is an indirect-object-like argument
            if self._has_iobject(V):
                return self.verb_classifier.classify([sc.NTRANS, sc.PTRANS], V.text)
            # Only two arguments means it is likely
            # a construct or destroy command
            else:
                return self.verb_classifier.classify([sc.CONS, sc.DESTROY], V.text)
        else:
            # If new variables are introduced,
            # we assume we have an observation type
            return sc.OBSERVATION
    
    def reset_variables_list(self):
        self.variables_list = []

    def _get_dobject_string(self, V):
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
        return "_".join([dobj.lemma_.lower()] + [m.lower() for m in mods])

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
        return "_".join([nsubj.lemma_.lower()] + [m.lower() for m in mods])

    def _get_iobject_string(self, V):
        """
        For ditransitive constructions, i.e. neg/pos transfer,
        there should be either an indirect object, or some indirect
        object like argument, oblique, nominal modifier, etc.
        """
        modifier_deps = ["amod", "nmod", "poss"]
        mods = []
        iobj = None
        
        for c in V.children:
            if c.dep_ in ["iobj", "nmod", "obl"]:
                iobj = c
                    
                mods += self._get_deps_strings(iobj,\
                                            [], modifier_deps)

        if not iobj:
            """
            We have observed an incorrect parse that stanford parser
            produces when the direct object has adjectival modifiers
            and the indirect object is a proper noun. This hack is
            to counteract that scenario, in which the proper noun gets
            tacked onto the directo object as a compound
            """
            for c in V.children:
                if c.dep_ == "dobj":
                    iobj = [cp for cp in c.children\
                            if cp.pos_ in ["PROPN", "NOUN"] and cp.dep_ == "compound"][0]

        return "_".join([iobj.lemma_.lower()] + [m.lower() for m in mods])

    def _has_iobject(self, V):
        modifier_deps = ["amod", "nmod", "poss"]
        mods = []
        iobj = None

        for c in V.children:
            if c.dep_ in ["iobj", "nmod", "obl"]:
                iobj = c

                mods += self._get_deps_strings(iobj,\
                                            [], modifier_deps)

        if not iobj:
            """                                                                                                                                       
            We have observed an incorrect parse that stanford parser                                                                                  
            produces when the direct object has adjectival modifiers                                                                                  
            and the indirect object is a proper noun. This hack is                                                                                    
            to counteract that scenario, in which the proper noun gets                                                                                
            tacked onto the directo object as a compound                                                                                              
            """
            for c in V.children:
                if c.dep_ == "dobj":
                    iobj = [cp for cp in c.children\
                            if cp.pos_ in ["PROPN", "NOUN"] and cp.dep_ == "compound"]
                    if len(iobj) != 0:
                        iobj = iobj[0]
                    else:
                        iobj = None

        if iobj is not None:
            return True
        else:
            return False
        
    def _get_quantifier(self, tokens):
        """
        We assume each sentence has exactly one quantifier
        """
        for token in tokens:
            if self._is_quantifier(token):
                return token

    def _is_quantifier(self, token):
        QUANTIFIER_STRINGS = ["some", "many", "few", "much", "several", "every", "all", "any"]

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
        # self.variables_list = []
        for label, sentence in zip(labels, sentences):
            tokens = self.get_tokens(sentence)
            if label == sc.OBSERVATION:
                commands.append([sc.OBSERVATION] + self.get_observation_arguments(tokens))
            elif label == sc.DESTROY:
                commands.append([sc.DESTROY] + self.get_destroy_arguments(tokens))
            elif label == sc.GET:
                commands.append([sc.GET] + self.get_get_arguments(tokens))
            elif label == sc.NTRANS:
                commands.append([sc.NTRANS] +\
                            self.get_negative_transfer_arguments(tokens))
            elif label == sc.PTRANS:
                commands.append([sc.PTRANS] +\
                            self.get_positive_transfer_arguments(tokens))
        return commands

    def add_to_variables_list(self, variable):
        if variable not in self.variables_list:
            self.variables_list.append(variable)

if __name__=='__main__':
    # Test _get_deps_strings
    # x = AlgebraNLP(use_stanford=False)
    x = AlgebraNLP(use_stanford=True)
    s1 = u"Pooja has 3 apples"
    s2 = u"Pooja eats one apple"
    scons = u"Pooja gets one apple"
    s3 = u"Pooja gives John 1 green apple"
    s4 = u"Pooja takes 5 green apple from John"
    s5 = u"How many green apples does Pooja have?"
    s6 = u"John has 4 apples"
    print x.get_commands([s1, s2, scons, s3, s4, s5, s6], [sc.OBSERVATION, sc.DESTROY, sc.CONS, sc.NTRANS, sc.PTRANS, sc.GET, sc.OBSERVATION])
