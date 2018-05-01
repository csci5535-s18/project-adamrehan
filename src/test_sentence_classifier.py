from sentence_classifier import VerbClassifier

classifier = VerbClassifier()

print(classifier.classify(["construct", "destroy"], ["eats"]))
