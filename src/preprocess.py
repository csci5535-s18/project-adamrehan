'''
Major thing to do here is to fill in the missing containers in the text through co-ref resolver, etc.
'''
from neuralcoref import Coref
coref = Coref()

def preprocess(anlp, text):
    '''
    This function takes in an entire word problem and
    splits into segments with relevent information to the algebra.
    It then performs coreference and turns all string numbers, like
    "twenty two" into a numeral format, like "22".

    This creates more usable chunks of text for anlp to parse.

    Todo: coref
    :param anlp:
    :param text:
    :return:
    '''
    clusters = coref.one_shot_coref(utterances=u"She loves him.", context=u"My sister has a dog.")
    mentions = coref.get_mentions()
    print(mentions)
    return ['Pooja has 3 apples', 'Pooja eats 1 apple', 'How many apples does Pooja have now?']

preprocess(1, 2)
