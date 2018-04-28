from aimp_generator import generate_aimp
from anlp import AlgebraNLP
from preprocess import preprocess
import sentence_classifier
import pickle
import numpy as np

anlp = AlgebraNLP()
classifier = sentence_classifier.load('verbs.clf')

OBSERVATION = 'observation'
CONS = 'construct'
PTRANS = 'p_transfer'

def prob2imp(text):
    sentences = preprocess(anlp, text)
    labels = classifier.predict_labels(sentences)
    commands = []
    for label, sentence in zip(labels, sentences):
        if label == OBSERVATION:
            commands.append([OBSERVATION] + anlp.get_observation_arguments(sentence))



if __name__=='__main__':
    prob = "Pooja has three apples. She eats one. How many apples does Pooja have now?"
    a_code = prob2imp(prob)
