from aimp_generator import generate_aimp
from anlp import AlgebraNLP
from preprocess import preprocess
import sentence_classifier

anlp = AlgebraNLP(use_stanford=True)
classifier = sentence_classifier.load('verbs.clf')

def prob2imp(text):
    sentences = preprocess(anlp, text)
    labels = classifier.predict_labels(sentences)
    commands = anlp.get_commands(sentences, labels)
    print generate_aimp(commands)

if __name__=='__main__':
    prob = u'Pooja has three apples. She eats one. How many apples does Pooja have now?'
    a_code = prob2imp(prob)
