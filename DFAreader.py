import NFAtoDFA
import string
import sys
import re


def bold(strng):
    return '\033[1m' + strng + '\033[0m'


def underline(strng):
    return '\033[4m' + strng + '\033[0m'


def get_string():
    print('Digit or paste C code here. Must hit ENTER per line to be read! \nUse CTRL + D to stop.')
    s = sys.stdin.read()
    s = s.splitlines()
    s = ' '.join(s)
    spec = re.compile(r"([,;(){}+*/-])")
    s = spec.sub(" \\1 ", s).split(' ')
    s = list(filter(None, s))
    return s

str_states = NFAtoDFA.str_states
low_letters = string.ascii_lowercase
letters = string.ascii_letters
nums = string.digits
chars = letters + nums

NFA = NFAtoDFA.NFA
finals = NFAtoDFA.finals

DFA = NFAtoDFA.toDFA(NFA)
start = next(iter(DFA))
tokens_list = []
strings = get_string()

for string in strings:  # Getting each individual string
    actstate = start
    lines = DFA.get(actstate)[0]
    states = DFA.get(actstate)[1]
    no_transition = True
    for char in string:
        no_transition = True
        ind = 0
        for line in lines:
            if char in line:
                no_transition = False
                break
            ind += 1
        if no_transition and actstate in str_states and actstate and char in chars:
            actstate = 'q32'
            lines = DFA.get(actstate)[0]
            states = DFA.get(actstate)[1]
            no_transition = False
        elif no_transition:
            break
        else:
            actstate = states[ind]
            lines = DFA.get(actstate)[0]
            states = DFA.get(actstate)[1]
    if actstate not in finals and actstate in str_states:
        tokens_list.append(finals.get('q32'))
    elif no_transition or actstate not in finals:
        tokens_list.append('ERROR')
    else:
        tokens_list.append(finals.get(actstate))

print(' '.join(tokens_list))
