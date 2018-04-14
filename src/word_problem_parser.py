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

def extract_commands(parsed_text):
    for token in parsed_text:
        if is_quantifier(token):
            print(get_parent_verb(token).text)

if __name__=='__main__':
    parser = argparse.ArgumentParser("Word Problem Parser")
    parser.add_argument('text', metavar='text', help=\
                        'The text of the word problem we are solving')
    args = parser.parse_args()
    text = args.text

    parsed_text = nlp(u'%s' % text)

    
    extract_commands(parsed_text)
