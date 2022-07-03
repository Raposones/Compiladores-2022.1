import pandas as pd

def_num = 1
defs = {}
vars_defs = {}
in_out = {}
gens_kills = {}
blocks = {}
prev_block = {1: []}
end_blocks = []


def get_gen_kills(bl):
    gen = []
    kill = []
    bl_lines = bl[0]
    for lin in bl_lines:
        lin = lin.split(': ')
        line_def = lin[0]
        gen.append(line_def)
        line_var = lin[1].split(' = ')[0]
        list_aux = vars_defs.get(line_var)
        line_var_defs = list_aux[:]
        line_var_defs.remove(line_def)
        for df in line_var_defs:
            kill.append(df)
    return gen, list(set(kill))


def get_in_out():
    dict_aux = {}
    global in_out
    while True:
        for num in range(1, len(blocks) + 1):
            b_gen_kill = gens_kills.get(num)
            b_gen = b_gen_kill[0]
            b_kill = b_gen_kill[1]
            b_prev = prev_block.get(num)
            b_in = []
            for v in b_prev:
                if v in dict_aux:
                    b_in.extend(dict_aux.get(int(v))[1])
            b_in = list(set(b_in))
            b_out = list(set(b_gen + [x for x in b_in if x not in b_kill]))
            dict_aux[num] = (b_in, b_out)
        if dict_aux == in_out:
            break
        in_out = dict_aux


f = open('input.txt', 'r')


while True:
    block = []
    line = f.readline()
    if line == '':
        break
    line = line.split(' ')
    block_num = int(line[0])
    block_n_lines = int(line[1])
    for i in range(block_n_lines + 1):
        aux = next(f).rstrip(' \n')
        if i == block_n_lines:
            ver = aux.split(' ')
            ver = [int(x) for x in ver]
            if max(ver) <= block_num:
                end_blocks.append(block_num)
            for v in [x for x in ver if x != 0]:
                if v in prev_block:
                    aux = prev_block.get(v)
                    aux.append(block_num)
                    prev_block[v] = aux
                else:
                    prev_block[v] = [block_num]
        else:
            block.append(f'd{def_num}: {aux}')
            defs[f'd{def_num}'] = aux
            var = aux.split(' = ')[0]
            if var in vars_defs:
                a = vars_defs.get(var)
                a.append(f'd{def_num}')
                vars_defs[var] = a
            else:
                vars_defs[var] = [f'd{def_num}']
            def_num += 1
    blocks[block_num] = (block, ver)
aux = prev_block.get(1)
aux.extend(end_blocks)
prev_block[1] = aux


for n in range(1, len(blocks) + 1):
    b = blocks.get(n)
    in_out[n] = ([], [])
    gens_kills[n] = get_gen_kills(b)

get_in_out()

b_gen = []
b_kill = []
b_ins = []
b_outs = []

for n in range(1, len(blocks) + 1):
    b_gen.append(gens_kills.get(n)[0])
    b_kill.append(gens_kills.get(n)[1])
    b_ins.append(in_out.get(n)[0])
    b_outs.append(in_out.get(n)[1])

df = pd.DataFrame({'gen': b_gen, 'kill': b_kill, 'in': b_ins,
                  'out': b_outs}, index=['B' + str(n) for n in blocks])
print(df.to_markdown())
