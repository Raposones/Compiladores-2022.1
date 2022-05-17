import pandas as pd


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_all_states(st_dict):
    for st in st_dict:
        print_state(states.get(st), st)


def print_table(tb):
    print(color.BLUE + 'LR(1) table for given grammar' + color.END)
    df = pd.DataFrame.from_dict(tb, orient='index').reset_index(drop=True)
    print(df.to_markdown(index=True))
    print('\n')


def print_state(st, st_num):
    st_actions = check_state_actions(st)
    print(color.BLUE + f'State {st_num}' + color.END)
    print('────────────────────')
    for transition in st:
        print(color.CYAN + f'{transition[0]} | {transition[1]}' + color.END)
    print('────────────────────')
    print(color.BOLD + 'ACTIONS: ' + color.END)
    for action, lookahead in st_actions:
        if 'R' in action:
            print(color.GREEN + f'{action} in {lookahead}' + color.END)
        elif 'S' in action:
            print(color.YELLOW + f'{action} in {lookahead}' + color.END)
        elif 'G' in action:
            print(color.PURPLE + f'{action} in {lookahead}' + color.END)
    print('────────────────────' + '\n\n')


def check_state_actions(stt):
    actions = []
    for line in stt:
        line_trans = line[0]
        if line_trans[-1] == '.':
            aux = line_trans.rstrip('.')
            actions.append((f'R{grammar_rules.index(aux)}', line[1]))
    return check_next_state_number(stt, actions)


def check_next_chars(state):  # receive state, returns list of characters next to dot in state
    next_chars = []
    for derivation in state:
        derivation = derivation[0].split(' ')
        for char in derivation:
            if '.' in char and char[-1] != '.':
                next_chars.append(char.lstrip('.'))
    next_chars = list(dict.fromkeys(next_chars))  # this removes repeated elements
    return next_chars


def check_next_state_number(st, actions):  # receive state [list of tuples]
    next_chars = check_next_chars(st)
    if len(next_chars) != 0:
        for char in next_chars:
            next_transitions = []
            for transition in st:
                if '.' + char in transition[0]:
                    next_transitions.append(go_to(transition, char))
            for next_transition in next_transitions:
                next_transitions.extend(closure(next_transition))
            for ind, next_transition in enumerate(next_transitions):
                if '.ε' in next_transition[0]:
                    aux = next_transition[0].replace('.ε', 'ε.')
                    next_transitions[ind] = (aux, next_transition[1])
            next_transitions = list(dict.fromkeys(next_transitions))
            if next_transitions in states.values():
                target_state = list(states.keys())[list(states.values()).index(next_transitions)]
                if char in non_terminals:
                    actions.append((f'G{target_state}', char))
                else:
                    actions.append((f'S{target_state}', char))
            else:
                print('falho no ' + char)
    return actions


def go_to(der, char):  # receive tuple (derivation, lookahead), returns same tuple after moving dot
    deriv = der[0]
    deriv = deriv.split(' ')
    for ind, c in enumerate(deriv):
        if '.' in c and c[1:] == char:
            deriv[ind] = deriv[ind].lstrip('.')
            if ind == len(deriv) - 1:  # if last char in derivation; no index after
                deriv[ind] += '.'
                deriv = ' '.join(deriv)
                return deriv, der[1]
            else:
                deriv[ind + 1] = '.' + deriv[ind + 1]
                deriv = ' '.join(deriv)
                return deriv, der[1]


def closure(deriv):  # receive tuple (derivation, lookahead), returns list of tuples after closure (empty if no closure)
    deriv_str = deriv[0].split(' ')
    lookahead = deriv[1]
    closure_derivs = []
    for ind, char in enumerate(deriv_str):
        if '.' in char and char[1:] in non_terminals:
            nt_derivs = grammar.get(char[1:])
            if ind == len(deriv_str) - 1:
                for nt_deriv in nt_derivs:
                    closure_derivs.append((f'{char[1:]} -> .' + nt_deriv, lookahead))
            else:
                char_lookahead = deriv_str[ind + 1]
                for nt_deriv in nt_derivs:
                    closure_derivs.append((f'{char[1:]} -> .' + nt_deriv, char_lookahead))
    for closure_deriv in closure_derivs:
        aux = closure_deriv[0].split(' ')
        for char in aux:
            if '.' in char and char[1:] in non_terminals:
                aux = closure(closure_deriv)
                for d in aux:
                    closure_derivs.append(d)
    return closure_derivs


def next_state(state, num):  # receive list of tuples (derivation, lookahead)
    global state_num
    # print(f'{num} -> {state}')
    next_transitions = check_next_chars(state)
    char_all_trans = []
    if len(next_transitions) != 0:
        for char in next_transitions:
            char_transitions = []
            for transition in state:
                if '.' + char in transition[0]:
                    char_transitions.append(go_to(transition, char))
            char_all_trans.append((char_transitions, char))
        for trans in char_all_trans:
            new_transitions = trans[0]
            new_closure = []
            for new_transition in new_transitions:
                new_closure.extend(closure(new_transition))
            new_transitions.extend(new_closure)
            for ind, new_transition in enumerate(new_transitions):
                if '.ε' in new_transition[0]:
                    aux = new_transition[0].replace('.ε', 'ε.')
                    new_transitions[ind] = (aux, new_transition[1])
            new_transitions = list(dict.fromkeys(new_transitions))
            if new_transitions not in states.values():
                states[state_num] = new_transitions
                state_num += 1
                next_state(new_transitions, state_num)





grammar = {'S': ['B'],
           'B': ['id P', 'id ( E ]'],
           'P': ['ε', '( E )'],
           'E': ['B', 'B , E']}

grammar_rules = ['S -> B', 'B -> id P', 'B -> id ( E ]', 'P -> ε', 'P -> ( E )', 'E -> B', 'E -> B , E']

non_terminals = ['S', 'B', 'P', 'E']

terminals = ['id', '(', ')', ',', ']', '$']

symbols = terminals + non_terminals

states = {0: [('S -> .B', '$'),
              ('B -> .id P', '$'),
              ('B -> .id ( E ]', '$')]}

state_num = 1

next_state(states[0], state_num)


num_states = range(0, len(states))
table = {}
for n in num_states:
    columns = {}
    for s in symbols:
        columns[s] = ''
    table[n] = columns


for state in table:
    state_actions = check_state_actions(states.get(state))
    for act, lookahead in state_actions:
        table[state][lookahead] = act

table[1]['$'] = 'end'

print_all_states(states)
print_table(table)
