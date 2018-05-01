'''
Major thing to do here is to fill in the missing containers in the text through co-ref resolver, etc.
'''
from neuralcoref import Coref
from anlp import AlgebraNLP
coref = Coref()

def resolve_coref_neural(text):
    coref.one_shot_coref(utterances=text, context=text)
    return coref.get_resolved_utterances()

def get_children(root, parse):
    children = []
    node = root[2]
    for item in parse:
        parent = item[1]
        if node == parent:
            children.append(item)
    return children

def get_deps(node, parse):
    deps = [node]
    node_ind = node[2]
    for n in parse:
        if n[1] == node_ind and 'conj' not in n[0] and 'cc' not in n[0]:
            deps += get_deps(n, parse)
    return deps

def get_dobj_sentences(root, tokens, parse, nsubs, dobjs):
    sentences = []
    for nsub in nsubs:
        for dobj in dobjs:
            sent = [root]
            sent += get_deps(nsub, parse)
            sent += get_deps(dobj, parse)
            sent = sorted([item[2] for item in sent])
            sentences.append(' '.join([tokens[i-1].text for i in sent]))
    return sentences

def make_sentence(root, tokens, parse):
    roots = []
    dobjs = []
    nsubs = []
    for child_node in get_children(root, parse):
        dep = child_node[0]
        ind = child_node[2] - 1
        if 'conj' in dep and 'VERB' in tokens[ind].pos_:
            roots.append(child_node)
        elif 'dobj' in dep:
            dobjs.append(child_node)
        elif 'nsub' in dep:
            nsubs.append(child_node)
    sentences = []
    sentences += get_dobj_sentences(root, tokens, parse, nsubs, dobjs)
    if len(roots) == 0:
        pass
    else:
        for r in roots:
            sentences += make_sentence(r, tokens, parse)

    return sentences

def removed_and(tokens):
    ret_toks = []
    for i, tok in enumerate(tokens):
        if 'and' == tok.text.lower():
            if i > 0 and i < len(len(tokens)):
                if 'ADJ' in tokens[i-1].pos_ and 'ADJ' in tokens[i+1].pos_:
                    pass
                else:
                    ret_toks.append(tok)
        else:
            ret_toks.append(tok)
    return ret_toks

def break_conjunctions(text, anlp):
    docs = anlp.nlp(text)
    sentences = [sent.string.strip() for sent in docs.sents]
    ret_sentences = []
    for sent in sentences:
        tokens = anlp.nlp(sent)
        text = []
        for i, t in enumerate(tokens):
            if t.pos_ == "PROPN":
                if i == 0:
                    text.append("she")
                else:
                    text.append("me")
            else:
                text.append(t.text)
        text = unicode(' '.join(text))
        # tokens = anlp.nlp(text)
        stanford_parse = anlp.snlp.dependency_parse(text, enhanced=True)
        ret_sentences += make_sentence(stanford_parse[0], tokens, stanford_parse)
    return ret_sentences

def preprocess(text, anlp=AlgebraNLP(True)):
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

    resolved_text = resolve_coref_neural(text=text)
    broken_sentences = break_conjunctions(resolved_text[0], anlp)
    return broken_sentences

if __name__ == "__main__":
    print preprocess(text=u"Pooja and Roy have 2 small and green apples and 2 red apples and John has 3 red apples. She eats one apple.")
