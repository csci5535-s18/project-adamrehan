import argparse

import spacy
nlp = spacy.load('en')

def is_quantifier(token):
    """
    input: a SpaCy token
    return: boolean as to whether this token is a quantifier
        e.g. a number

    NOT SURE THIS METHOD IS NEEDED, HERE IN CASE WE NEED TO EXTEND
    TO THINGS THAT ARE NOT DIGITS.
    """
    return token.text.isdigit()

def get_parent_verb(token):
    """
    Get the verb that is the closest parent in this
    token's dependency tree, by recursing up the tree
    """
    def _get_parent_verb(t):
        if t.head.pos_ == "VERB":
            return t.head
        else:
            return _get_parent_verb(t.head)
    
    return _get_parent_verb(token)

def get_deps(t):
    deps_list=[]
    for c in t.children:
        deps_list.append((c.text, c.dep_, get_deps(c)))

    return deps_list
        
def extract_commands(parsed_text):
    for token in parsed_text:
        if is_quantifier(token):
            verb = get_parent_verb(token)
            print(get_deps(verb))

if __name__=='__main__':
    parser = argparse.ArgumentParser("Word Problem Parser")
    parser.add_argument('text', metavar='text', help=\
                        'The text of the word problem we are solving')
    args = parser.parse_args()
    text = args.text

    parsed_text = nlp(u'%s' % text)

    """
    Basic idea:

    Find a quantifier, and then find its closest parent that is
    a verb.
    Now, using a similarity metric, map that verb to some command
    The denotational semantics of that command should give us a sort of
    'template'. From here, we can fill that command template
    with args from the Verbs dependency tree. Will this scale
    to large expressions?
    """
    extract_commands(parsed_text)
