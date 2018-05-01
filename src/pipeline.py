from aimp_generator import generate_aimp
from anlp import AlgebraNLP
from preprocess import preprocess
import sentence_classifier

anlp = AlgebraNLP(use_stanford=True)
#classifier = sentence_classifier.load('verbs.clf')

def prob2imp(text):
    sentences = preprocess(text, anlp)
    commands = anlp.classify_and_get_sentences(sentences)
    # commands = anlp.get_commands(sentences, labels)
    return generate_aimp(commands)

if __name__=='__main__':
    # prob = u'Pooja has three apples. She eats one apple. How many apples does Pooja have now?'
    # print prob2imp(prob)
    prob = u'Pooja has three apples. John has one apple. Pooja gives one apple to John. How many apples does Pooja have now?'
    print prob2imp(prob)

