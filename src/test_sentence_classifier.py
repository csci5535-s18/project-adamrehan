from sentence_classifier import VerbClassifier

classifier = VerbClassifier()


pred2label = {"destroy": "d", "construct": "c"}
acc = 0
total = 0
for label, verbs in classifier.labeled_verbs.items():
    for v in verbs:
        pred = classifier.classify(["construct", "destroy"], [v])[0]
        target = label
        print(v)
        print("guess: %s" % pred)
        print("correct: %s" % label)
        if pred2label[pred] == label:
            acc += 1
            
        total += 1

print("ACC: %2f" % (acc / total))
