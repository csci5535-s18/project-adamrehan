'''
We would like to generate code for different languages from our intermediary language
For example to Language A-IMP, or python etc
'''
from sentence_classifier import OBSERVATION, CONS, DESTROY, GET, PTRANS, NTRANS
def set(args):
    a = args[0]
    e = args[1]
    return 'set[{a}]({e})'.format(a=a, e=e)

def seq(args):
    c1 = args[0]
    c2 = args[1]
    return 'seq({c1}; {c2})'.format(c1=c1, c2=c2)

def ptransfer(args):
    a1 = args[0]
    a2 = args[1]
    e = args[2]
    return seq([construct([a1, e]), destroy([a2, e])])

def ntransfer(args):
    a1 = args[0]
    a2 = args[1]
    e = args[2]
    return seq([destroy([a1, e]), construct([a2, e])])

def destroy(args):
    a = args[0]
    e = args[1]
    return set([a, 'minus(get({a}); {e})'.format(a=a, e=e)])

def construct(args):
    a = args[0]
    e = args[1]
    return set([a, 'add(get({a}); {e})'.format(a=a, e=e)])

def get(args):
    a = args[0]
    return 'get({})'.format(a)

def do_raise():
    raise LookupError

def match(command):
    c_type = command[0]
    args = command[1:]
    if c_type == OBSERVATION:
        return set(args)
    elif c_type == PTRANS:
        return ptransfer(args)
    elif c_type == NTRANS:
        return ntransfer(args)
    elif c_type == DESTROY:
        return destroy(args)
    elif c_type == CONS:
        return construct(args)
    elif c_type == GET:
        return get(args)
    else:
        return None

def generate_seq(commands):
    if len(commands) == 1:
        return commands[0]
    else:
        c1 = commands[0]
        return seq([c1, generate_seq(commands[1:])])

def generate_aimp(commands):
    imp_commands = []
    for com in commands:
        imp_commands.append(match(com))
    return generate_seq(imp_commands)

if __name__=='__main__':
    commands  = [[OBSERVATION, 'a', '3'], [DESTROY, 'a', '1'], [GET, 'a']]
    print generate_aimp(commands)