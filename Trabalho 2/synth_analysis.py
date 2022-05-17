import lr1_auto as lr1
import re
from tabulate import tabulate


grammar_rules = ['S -> B', 'B -> id P', 'B -> id ( E ]', 'P -> ε', 'P -> ( E )', 'E -> B', 'E -> B , E']
non_terminals = ['S', 'B', 'P', 'E']


def print_sequence():
    print(tabulate(final, headers=['Input', 'Stack', 'Action']))


def split_char_digit(s):  # returns [char, number]
    return re.findall(r'[A-Za-z$()ε,]+|\d+', s)


def shift(st, stk, next_char, next_state):
    stk.append(next_char + next_state)
    st.remove(next_char)
    return [st, stk]


def reduce(stk, next_state):
    rule = grammar_rules[int(next_state)].split(' -> ')
    if rule[1] != 'ε':
        stk = stk[: len(stk) - len(rule[1].split(' '))]  # this should remove the elements of rule based on its size
    prev_state = split_char_digit(stk[-1])[1]
    stk.append(rule[0] + prev_state)
    return stk


def synth_analysis(split_str, stk, state):
    global final
    act_string = ''
    stk_last_char = split_char_digit(stk[-1])
    if stk_last_char[0] in non_terminals:
        next_char = stk_last_char[0]
        nx = table[state][next_char]
        next_action_state = split_char_digit(nx)
    else:
        next_char = split_str[0]
        nx = table[state][next_char]
        next_action_state = split_char_digit(nx)
    if next_action_state == 'end':
        return True
    else:
        if not next_action_state:
            final.append([' '.join(split_str), ' '.join(stk), 'error'])
            return False
        else:
            next_act = next_action_state[0]
            next_state = next_action_state[1]
            if next_act == 'S':
                aux = shift(split_str, stk, next_char, next_state)
                split_str = aux[0]
                stk = aux[1]
                act_string = f'Shift {next_char}, go to {next_state}'
            elif next_act == 'R':
                stk = reduce(stk, next_state)
                act_string = f'Reduce {grammar_rules[int(next_state)]}'
            elif next_act == 'G':
                goto_action = table[int(next_state)][split_str[0]]
                goto_action_str = goto_action[0]
                goto_action_num = goto_action[1]
                if goto_action_str == 'S':
                    aux = shift(split_str, stk, split_str[0], goto_action_num)
                    split_str = aux[0]
                    stk = aux[1]
                    act_string = f'Shift {split_str[0]}, go to {goto_action_num}'
                elif goto_action_str == 'R':
                    stk = reduce(stk, goto_action_num)
                    act_string = f'Reduce {grammar_rules[int(goto_action_num)]}'
                elif goto_action == 'end':
                    final.append([' '.join(split_str), ' '.join(stk), 'accept'])
                    return True
            else:
                act_string = 'ERROR'
            final.append([' '.join(split_str), ' '.join(stk), act_string])
            stk_last_state = int(split_char_digit(stk[-1])[1])
            synth_analysis(split_str, stk, stk_last_state)


table = lr1.table
inp = input(lr1.color.YELLOW + 'Type the code to be analysed: ' + lr1.color.END)
inp_orig = inp
inp += ' $'

inp_list = inp.split(' ')
stack = ['$0']

a = [inp, ' '.join(stack), '']
final = [a]

analysis_check = synth_analysis(inp_list, stack, 0)
print_sequence()

check_acceptance = final[-1]
check_acceptance = check_acceptance[2]

if check_acceptance == 'accept':
    print(lr1.color.BOLD + f'\n{inp_orig}' + lr1.color.END + lr1.color.CYAN + ' accepted successfully' + lr1.color.END)
else:
    print(lr1.color.RED + '\nerror while analysing ' + lr1.color.END + lr1.color.BOLD + f'{inp_orig}' + lr1.color.END)
