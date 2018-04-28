'''
We would like to generate code for different languages from our intermediary language
For example to Language A-IMP, or python etc
'''

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
    return seq(
        [set(
            [a1,
             '{} + {}'.format(a1, e)
             ]),
        set(
            [a2,
             '{} - {}'.format(a2, e)
             ])
        ]
    )

OBS = 'observation'
CONS = 'construct'
PTRANS = 'p_transfer'
def do_raise():
    raise LookupError

def match(command):
    c_type = command[0]
    args = command[1:]

    if c_type == OBS:
        return set(args)
    elif c_type == PTRANS:
        return ptransfer(args)
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
    commands  = [[OBS, 'a1', '3'], [OBS, 'a2', '5'], [PTRANS, 'a1', 'a2', 1]]
    print generate_aimp(commands)