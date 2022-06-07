"""
I. se as operações usam tipos compatíveis
II. se as variáveis (e funções) estão sendo usadas dentro de seu escopo
III. se as variáveis (e funções) estão sendo usadas sem serem declaradas
"""

"""
!!!! Não funciona direito com atribuições de função: a atribuição deve conter a função PRIMEIRO!
a = f ( a, b ) funciona
a = f ( a , b ) + n funciona
a = 1 + f ( a , b ) NAO FUNCIONA :(
"""
import re
class colors:
    BLACK = '\33[30m'
    RED = '\33[31m'
    GREEN = '\33[32m'
    YELLOW = '\33[33m'
    BLUE = '\33[34m'
    VIOLET = '\33[35m'
    BEIGE = '\33[36m'
    WHITE = '\33[37m'
    END = '\33[0m'
    BOLD = '\33[1m'
    SELECTED = '\33[7m'

operation_chars = ['+', '-', '/', '*', '**', ',']
errors = 0

def check_used_vars(sc_vars, scp_atts, sc_num):
    for var_tup in sc_vars:
        used_var = False
        var = var_tup[0]
        if not any([var in tup for tup in form_funcs]):
            for att in scp_atts:
                att = att.split(' ')
                if var in att and att[0] != var:
                    used_var = True
                    break
            if not used_var:
                print(colors.BLUE + 'Variable ' + colors.SELECTED + var + colors.END +
                      colors.BLUE + f' is not used in scope {sc_num}.' + colors.END)


def evaluate_functions(sc_func, sc_num, line):
    global errors
    exists_func = False
    func_txt = ' '.join(sc_func)
    line_txt = ' '.join(line)
    aux = ()
    f_types = []
    for f in form_funcs:
        if sc_func[0] == f[0]:
            exists_func = True
            aux = f
            break
    if not exists_func:
        print(colors.RED + 'Non-existant function use in line ' + colors.SELECTED + line + colors.END)
        errors += 1
        return None
    else:
        aux_types = aux[2]
        f_vars = func_txt[func_txt.find("(")+1:func_txt.find(")")].split(' , ')
        for var in f_vars:
            var = var.lstrip(' ').rstrip(' ')
            f_types.append(check_var_type(var, scopes.get(sc_num), sc_num))
        if aux_types != f_types:
            print(colors.VIOLET + 'Wrong parameter type in line ' +
                  colors.SELECTED + line + colors.END)
            errors += 1
        return aux[1]


def evaluate_attributions(sc_atts, sc, sc_num):
    global errors
    out_scope = sc[1]
    evaluated = []
    types_txt = ''
    is_func = False
    for att in sc_atts:
        aux = att
        types_list = []
        att = att.split(' ')
        if att[0] == 'return':
            att = att[1:]
        else:
            att = att[2:]
            if '(' in att:
                if att[1] == '(':
                    types_list.append(evaluate_functions(att, sc_num, aux))
                    ind = att.index(')') + 1
                    att = att[ind:]
                    if len(att) == 0:
                        continue
                else:
                    att = ' '.join(att).replace(
                        '(', '').replace(')', '').split()
        for char in att:
            if char not in operation_chars:
                if char.isdigit():
                    c_type = 'int'
                    types_list.append(c_type)
                elif '"' in char:
                    c_type = 'char'
                    types_list.append(c_type)
                else:
                    c_type = check_var_type(char, sc, sc_num)
                    if c_type is None:
                        types_txt += colors.RED + 'Variable ' + colors.SELECTED + char + \
                            colors.END + colors.RED + \
                            ' is used without previous definition in line ' + \
                            colors.SELECTED + aux + colors.END + '\n'
                        errors += 1
                    types_list.append(c_type)
        if types_list.count(types_list[0]) != len(types_list):
            print(colors.VIOLET + 'Trying to do operation with different types in line: ' + colors.SELECTED
                  + aux + colors.END)
            errors += 1
        if None in types_list:
            types_txt = types_txt.rstrip('\n')
            print(types_txt)
        evaluated.append(types_list)
    return evaluated


def check_var_type(var, sc, scope_num):
    var_type = ''
    out_scope = sc[1]
    contains_var = False
    sc_vars = scopes_types.get(scope_num)
    if var.isdigit():
        return 'int'
    if '"' in var:
        return 'string'
    for vars_types in sc_vars:
        if var in vars_types:
            var_type = vars_types[1]
            contains_var = True
            return var_type
    if not contains_var:
        if scope_num != out_scope:
            check_var_type(var, scopes.get(out_scope), out_scope)
        else:
            return None


def check_inside_brackets(st, parent_block):
    st = st.split(' ')
    inside_bracket = False
    inside_block = []
    aux = 0
    for word in st:
        if inside_bracket:
            if word == '}':
                inside_bracket = False
            else:
                inside_block.append(word)
        else:
            if word == '{' and aux == 0:
                aux += 1
            elif word == '{' and aux > 0 and 'if' not in st and 'else' not in st:
                inside_bracket = True
    if len(inside_block) != 0:
        inside_block = ' '.join(inside_block)
        return (inside_block, parent_block)


def check_scope_types(sc):
    scope_data = sc[0].split(' ')
    scope_var_types = []
    for ind, word in enumerate(scope_data):
        if word in ('int', 'string'):
            scope_var_types.append((scope_data[ind + 1], word))
    return scope_var_types


def check_block_attributions(sc):
    scope_data = sc[0].split(' ')
    scope_att = []
    str_att = ''
    get_char = False
    for ind, word in enumerate(scope_data):
        if word == 'return':
            str_att += f'{word}'
            get_char = True
        elif word == '=':
            str_att += f'{scope_data[ind - 1]} {word}'
            get_char = True
        elif get_char is True and word != ';':
            str_att += f' {word}'
        elif get_char is True and word == ';':
            scope_att.append(str_att)
            str_att = ''
            get_char = False
    return scope_att


def check_operation(sc_att):
    aux = ''
    for att in sc_att:
        if '=' in att:
            aux = att[4:]
        elif 'return' in att:
            aux = att[2:]


def check_operations(sc_att, sc_vars):
    var_type = ''
    checked_vars = []
    for att in sc_att:
        var_att = att.split(' = ')
        for vars_types in sc_vars:
            if var_att[0] in vars_types:
                var_type = vars_types[1]
                checked_vars.append(f'{var_att[0]} is type {var_type}')
    print(checked_vars)


code_txt = open("code.txt", "r")
code_lines = []
functions = []
form_funcs = []
sig_num = 1

for line in code_txt:
    code_lines.append(line.rstrip('\n').lstrip('\t'))

code = ' '.join(code_lines)
code = re.sub(' +', ' ', code)

block = []
blocks = []
outer_scope = ''
inside_scope = False
nested_braces = 0

for line in code_lines:
    aux = line.split(' ')
    if '{' in line and not inside_scope:
        block.append(line)
        inside_scope = True
    elif '{' in line and inside_scope:
        block.append(line)
        nested_braces += 1
    elif '}' in line and nested_braces >= 1:
        block.append(line)
        nested_braces -= 1
    elif '}' in line and nested_braces == 0:
        block.append(line)
        block = ' '.join(block)
        blocks.append(block)
        block = []
        inside_scope = False
    elif inside_scope:
        block.append(line)
    elif not inside_scope:
        outer_scope += f' {line}'
    if '(' in aux:
        if aux[2] == '(' and aux[0] == 'int' or aux[0] == 'string':
            functions.append(line)

outer_scope = re.sub(' +', ' ', outer_scope)
outer_scope = outer_scope.rstrip(' ').lstrip(' ')

for f in functions:
    aux = f.rstrip('{').split()
    func_type = aux[0]
    func_name = aux[1]
    func_vars = f[f.find("(")+1:f.find(")")].split(' , ')
    vars_types = []
    for func_var in func_vars:
        if 'int' in func_var:
            vars_types.append('int')
        elif 'string' in func_var:
            vars_types.append('string')
    func = (func_name, func_type, vars_types)
    form_funcs.append(func)


scopes = {}
scopes_types = {}
scopes_attributions = {}

scopes[0] = (outer_scope, 0)
for block in blocks:
    scopes[sig_num] = (block, 0)
    sig_num += 1

inside_blocks = []

for n in range(0, len(scopes)):
    aux = scopes.get(n)
    inside_block = check_inside_brackets(aux[0], n)
    if inside_block is not None:
        scopes[sig_num] = inside_block
        sig_num += 1


for n in range(0, len(scopes)):
    aux = scopes.get(n)
    scope_types = check_scope_types(aux)
    scope_attributions = check_block_attributions(aux)
    scopes_types[n] = scope_types
    scopes_attributions[n] = scope_attributions


for n in range(0, len(scopes)):
    sc = scopes.get(n)
    sc_types = scopes_types.get(n)
    sc_atts = scopes_attributions.get(n)
    evaluated_atts = evaluate_attributions(sc_atts, sc, n)
    check_used_vars(sc_types, sc_atts, n)

if errors > 0:
    print(colors.YELLOW + str(errors) + ' errors found.' + colors.END)
else:
    print(colors.GREEN + 'Success!' + colors.END)

code_txt.close()
