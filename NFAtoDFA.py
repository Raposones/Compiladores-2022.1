import string


def bold(strng):
    return '\033[1m' + strng + '\033[0m'


def underline(strng):
    return '\033[4m' + strng + '\033[0m'


def isNondeter(state1):    # considering the case where non-determinism is defined only by having 'ε' (as the other case [multiple lines for one entry] is not used.
    if 'ε' in state1:
        return True


def toDFA(nfa):
    print('Converting NFA into DFA...\n')
    usedstates = []
    dfa = {}
    for state2 in nfa:
        used_lowletters = []
        nonused_lowletters_list = list(low_letters)
        nonused_lowletters = ''
        nonused_chars_list = list(chars)
        nonused_chars = ''
        trans = nfa.get(state2)[0]    # for each state, get its transitions (lines)
        if isNondeter(trans):
            statesclosure = []
            normal_transitions = []
            normal_states = []
            state_trans = nfa.get(state2)[1]
            trans_ind = 0
            for line_transition in trans:
                if line_transition == 'ε':
                    statesclosure.append(state_trans[trans_ind])
                else:
                    normal_transitions.append(trans[trans_ind])
                    normal_states.append(state_trans[trans_ind])
                trans_ind += 1
            newstate = ' '.join(statesclosure)
            newstate_lines = []
            newstate_transitions = []
            for stateaux in statesclosure:
                newstate_lines.extend(nfa.get(stateaux)[0])
                newstate_transitions.extend(nfa.get(stateaux)[1])
            usedstates.extend(statesclosure)
            used_lowletters.extend(newstate_lines)
            for item in used_lowletters:                        # The two for-loop removes low case characters consumed by other lines in the alphabet.
                if item in nonused_lowletters_list:             # This would cause a non-determinism by repeating the same character on transitions,
                    nonused_lowletters_list.remove(item)        # leading to multiple states at once (ex: q0 -- 'a' -> q1; q0 -- '[b-z]' -> q2)
                    nonused_lowletters = ''.join(nonused_lowletters_list)
            for line1 in newstate_lines:
                if line1 is low_letters:
                    ind1 = newstate_lines.index(line1)
                    newstate_lines[ind1] = nonused_lowletters
            newstate_lines.extend(normal_transitions)
            newstate_transitions.extend(normal_states)
            dfa[newstate] = [newstate_lines, newstate_transitions]
        else:
            if state2 not in usedstates:
                state_lines = nfa.get(state2)[0]
                if chars in state_lines:                                        # Same character removal from alphabet, but outside non-deterministic states
                    for lineaux in state_lines:
                        if lineaux in low_letters and lineaux != low_letters:
                            used_lowletters.append(lineaux)
                    for used_letter in used_lowletters:
                        if used_letter in nonused_chars_list:
                            nonused_chars_list.remove(used_letter)
                    nonused_chars = ''.join(nonused_chars_list)
                    letters_ind = state_lines.index(chars)
                    state_lines[letters_ind] = nonused_chars
                dfa[state2] = nfa.get(state2)
    return dfa


def printAutom(auto):
    for state in auto:
        finalst = False
        lines = auto.get(state)[0]
        states = auto.get(state)[1]
        if state in finals:
            print('State: ' + bold(state) + ' [final]')
            finalst = True
        else:
            print('State: ' + bold(state))
        ind = 0
        for line in lines:
            if states[ind] != '' and line != '':
                print('-> Goes to state ' + bold(states[ind]) + ' consuming ' + bold(line))
            else:
                print('-> No transition.')
            ind += 1
        if finalst:
            token = finals.get(state)
            print('» Final state for ' + underline(token) + ' token')
        print('\n')


def returnDFA(nfa):
    dfa = toDFA(nfa)
    return dfa


low_letters = string.ascii_lowercase
letters = string.ascii_letters
nums = string.digits
chars = letters + nums

NFA = {'q0': [['ε', 'ε', 'ε', 'ε', 'ε', 'ε', 'ε', 'ε', 'ε', 'ε', 'ε'], ['q1', 'q6', 'q11', 'q16', 'q22', 'q29', 'q31', 'q33', 'q50', 'q55', 'q60']],
       'q1': [['i'], ['q2']], 'q2': [['f', 'n'], ['q3', 'q4']], 'q3': [[''], ['']], 'q4': [['t'], ['q5']],
       'q5': [[''], ['']],
       'q6': [['e'], ['q7']], 'q7': [['l'], ['q8']], 'q8': [['s'], ['q9']], 'q9': [['e'], ['q10']], 'q10': [[''], ['']],
       'q11': [['v'], ['q12']], 'q12': [['o'], ['q13']], 'q13': [['i'], ['q14']], 'q14': [['d'], ['q15']],
       'q15': [[''], ['']],
       'q16': [['f'], ['q17']], 'q17': [['l'], ['q18']], 'q18': [['o'], ['q19']], 'q19': [['a'], ['q20']],
       'q20': [['t'], ['q21']], 'q21': [[''], ['']],
       'q22': [['r'], ['q23']], 'q23': [['e'], ['q24']], 'q24': [['t'], ['q25']], 'q25': [['u'], ['q26']],
       'q26': [['r'], ['q27']], 'q27': [['n'], ['q28']], 'q28': [[''], ['']],
       'q29': [[nums], ['q30']], 'q30': [[nums, '.'], ['q30', 'q67']], 'q67': [[nums], ['q68']], 'q68': [[nums], ['q68']],
       'q31': [[low_letters], ['q32']], 'q32': [[chars], ['q32']],
       'q33': [['=', '!', ',', ';', '(', ')', '{', '}', '+', '-', '*', '/'], ['q34', 'q35', 'q40', 'q41', 'q42', 'q43', 'q44', 'q45', 'q46', 'q47', 'q48', 'q49']],
       'q34': [['='], ['q36']], 'q35': [['='], ['q38']], 'q38': [[''], ['']],
       'q36': [[''], ['']],
       'q40': [[''], ['']], 'q41': [[''], ['']], 'q42': [[''], ['']], 'q43': [[''], ['']], 'q44': [[''], ['']], 'q45': [[''], ['']],
       'q46': [[''], ['']], 'q47': [[''], ['']], 'q48': [[''], ['']], 'q49': [[''], ['']],
       'q50': [['m'], ['q51']], 'q51': [['a'], ['q52']], 'q52': [['i'], ['q53']], 'q53': [['n'], ['q54']], 'q54': [[''], ['']],
       'q55': [['c'], ['q56']], 'q56': [['h'], ['q57']], 'q57': [['a'], ['q58']], 'q58': [['r'], ['q59']], 'q59': [[''], ['']],
       'q60': [['s'], ['q61']], 'q61': [['t'], ['q62']], 'q62': [['r'], ['q63']], 'q63': [['i'], ['q64']], 'q64': [['n'], ['q65']], 'q65': [['g'], ['q66']], 'q66': [[''], ['']],
       }

start = 'q0'
finals = {'q3': 'IF', 'q5': 'INT', 'q10': 'ELSE', 'q15': 'VOID', 'q21': 'FLOAT',
          'q28': 'RETURN', 'q30': 'NUM', 'q32': 'ID', 'q34': 'EQ', 'q36': 'ISEQ', 'q38': 'NOTEQ',
          'q40': 'COMMA', 'q41': 'SEMI', 'q42': 'LP', 'q43': 'RP', 'q44': 'LB', 'q45': 'RB',
          'q46': 'ADD', 'q47': 'SUB', 'q48': 'MULT', 'q49': 'DIV', 'q54': 'MAIN',
          'q59': 'CHAR', 'q66': 'STRING', 'q68': 'FLOATNUM'
          }
str_states = ['q2', 'q3', 'q4', 'q5', 'q7', 'q8', 'q9', 'q10', 'q12', 'q13', 'q14', 'q15', 'q17', 'q18', 'q19', 'q20', 'q21', 'q23', 'q24', 'q25', 'q26',
              'q27', 'q28', 'q51', 'q52', 'q53', 'q54', 'q56', 'q57', 'q58', 'q59', 'q61', 'q62', 'q63', 'q64', 'q65', 'q66']



