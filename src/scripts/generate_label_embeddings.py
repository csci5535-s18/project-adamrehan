# We want one embedding for VN Classes that have the predicate
# has_possession(end(E), Agent, X)
# And we want one embedding for classes that have the predicate
# has_possession(end(E), X != Agent, Y)

"""
from bs4 import BeautifulSoup as soup
import verbnet
verbnet_folder = "/home/adam/autoextendVN/data/verbnet3.3/"
ch_of_poss_predicate = [verbnet.Predicate(soup('<PRED value="path_rel"><ARGS><ARG type="Constant" value="ch_of_poss"/><ARG type="Event" value="end(E)"/><ARG type="ThemRole" value="Recipient"></ARGS></PRED>', 'lxml-xml').PRED)]
ch_of_loc_predicate = [verbnet.Predicate(soup('<PRED value="path_rel"><ARGS><ARG type="Constant" value="ch_of_loc"/><ARG type="Event" value="end(E)"/><ARG type="ThemRole" value="Recipient"></ARGS></PRED>', 'lxml-xml').PRED)]

if __name__=='__main__':
    vn = verbnet.VerbNetParser(directory=verbnet_folder)

    for vnc in vn.get_verb_classes():
        for frame in vnc.frames:
            if frame.contains(ch_of_poss_predicate) or frame.contains(ch_of_loc_predicate):
                print(frame.class_id(subclasses=False))

#            elif frame.contains(test):
#                print("TEST")
#                print(frame.class_id(subclasses=False))
            #elif frame.contains(destroy_predicate):       
    
#    def get_construct_classes():
#        for vnc in vn.get_verb_classes():

#    def get_destroy_classes():
"""
import torch
import numpy as np
import pickle

VNCEMBEDS = C = torch.load("/home/adam/autoextendVN/embed_mappings/C")
class2id = pickle.load(open("/home/adam/autoextendVN/embed_mappings/class2id", "rb"))
# VerbNet has failed us. I will manually procure a list
destroy_classes = ["throw-17.1", "give-13.1", "pay-68", "send-11.1"]
construct_classes = ["get-13.5.1", "fulfilling-13.4.1", "obtain-13.5.2"]
DIMS = 300

destroy_mat = torch.FloatTensor(len(destroy_classes), DIMS)
for i, d in enumerate(destroy_classes):
    destroy_mat[i] = C[class2id[d]]

construct_mat = torch.FloatTensor(len(construct_classes), DIMS)
for i, c in enumerate(construct_classes):
    construct_mat[i] = C[class2id[c]]

# Get the average embedding of all 'destroy' classes
#destroy_embed = torch.sum(destroy_mat, 0) / destroy_mat.size(0)
#destroy_embed = destroy_embed.cpu().numpy()

# Get the average embedding of all 'constrict' classes
#construct_embed = torch.sum(construct_mat, 0) / construct_mat.size(0)
#construct_embed = construct_embed.cpu().numpy()

destroy_mat = destroy_mat.cpu().numpy()
construct_mat = construct_mat.cpu().numpy()

np.save("../embeddings/destroy_matrix", destroy_mat)
np.save("../embeddings/construct_matrix", construct_mat)
