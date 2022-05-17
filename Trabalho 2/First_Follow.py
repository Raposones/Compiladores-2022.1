""" Gramática original (há recursão à esquerda):
S -> B $    B -> id P           P -> ε          E -> B
            B -> id ( E )       P -> ( E )      E -> B , E
"""

from tabulate import tabulate

grammar = {'S': ['B'],
           'B': ['id P', 'id ( E )'],
           'P': ['ε', '( E )'],
           'E': ['B', 'B , E']}

non_terminals = ['S', 'B', 'P', 'E']
terminals = ['ε', 'id', '(', ')', ',', '$']
start = 'S'


def print_table(lst):
    print(tabulate(lst, headers=['Non Terminal', 'First', 'Follow']))


def is_nullable(derivations):
    nullable = False
    for derivation in derivations:
        if 'ε' in derivation:
            nullable = True
    return nullable


def first(a, first_list=None):
    if first_list is None:  # this doesnt let the list reset every call
        first_list = []
    if a in terminals:
        first_list.append(a)
    else:
        a_derivations = grammar.get(a)  # derivations LIST where 'a' can lead into
        for a_derivation in a_derivations:  # every SINGLE derivation from above list
            a_derivation_list = a_derivation.split(' ')
            for char in a_derivation_list:  # every SINGLE char from above derivation
                if char == a:
                    break
                elif char in terminals:
                    first_list.append(char)
                    break  # breaking derivation char verification: terminal already found
                else:
                    char_derivations = grammar.get(char)
                    if is_nullable(char_derivations) and not a_derivation_list[-1] == char:  # if derivations from char contains ε and isnt last char in derivation
                        next_char_ind = a_derivation_list.index(char) + 1
                        first(a_derivation_list[next_char_ind], first_list)
                    first(char, first_list)
                    break
    first_list = [item for item in first_list if item != 'ε']
    first_list = list(dict.fromkeys(first_list))
    return first_list


def follow(a, follow_list=None):
    if follow_list is None:  # this doesnt let the list reset every call
        follow_list = []
    gram = grammar.items()
    if a is start:
        follow_list.append('$')
    for non_term, strings in gram:
        for string in strings:
            string_list = string.split(' ')
            for char in string_list:
                if char == a:
                    if char == string_list[-1] and char != non_term:
                        follow(non_term, follow_list)
                    elif char != string_list[-1]:
                        next_char_ind = string_list.index(char) + 1
                        follow_aux = first(string_list[next_char_ind])
                        follow_list.extend(follow_aux)
                        if 'ε' not in follow_aux:
                            break

    follow_list = [item for item in follow_list if item != 'ε']
    follow_list = list(dict.fromkeys(follow_list))
    return follow_list


final = []
for nt in non_terminals:
    results = [nt, ' '.join(first(nt)), ' '.join(follow(nt))]
    final.append(results)

print_table(final)
