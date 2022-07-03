import pandas as pd

blocks = {}
blocks_expr = {}
prev_block = {1: []}
gen_kill = {}
in_out = {}
end_blocks = []
all_expr = []


def get_gen_kill(b, b_expr):
    b_lines = b[0]
    gen = []
    kill = []
    for ind, expr in enumerate(b_expr):
        live = True
        for line in b_lines[ind:]:
            line = line.split(' = ')
            line_var = line[0]
            line_expr = line[1]
            if line_var in expr:
                live = False
            if line_expr == expr:
                live = True
        if live:
            gen.append(expr)
        else:
            kill.append(expr)
    return gen, kill


def get_in_out():
    dict_aux = {}
    global in_out
    while True:
        for num in range(1, len(blocks) + 1):
            b_gen_kill = gen_kill.get(n)
            b_gen = b_gen_kill[0]
            b_kill = b_gen_kill[1]
            b_prev = prev_block.get(n)
            b_in = []
            for prev in b_prev:
                b_in.extend(in_out.get(prev)[1])
            b_in = list({x for x in b_in if b_in.count(x) == len(b_prev)})
            b_out = list(set(b_gen + [x for x in b_in if x not in b_kill]))
            dict_aux[num] = (b_in, b_out)
        if dict_aux == in_out:
            break
        in_out = dict_aux


f = open('input.txt', 'r')

while True:
    block_expr = []
    block_line = []
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
            block_line.append(aux)
            aux = aux.split(' = ')
            expr = aux[1]
            expr_aux = expr.split(' ')
            if len([x for x in expr_aux if x.isalnum() and not x.isdigit()]) > 0:
                block_expr.append(expr)
                all_expr.append(expr)
    blocks_expr[block_num] = block_expr
    blocks[block_num] = (block_line, ver)
aux = prev_block.get(1)
aux.extend(end_blocks)
prev_block[1] = aux
all_expr = list(set(all_expr))

for n in range(1, len(blocks) + 1):
    bl = blocks.get(n)
    bl_expr = blocks_expr.get(n)
    gen_kill[n] = get_gen_kill(bl, bl_expr)
    bl_kill = gen_kill.get(n)[1]
    in_out[n] = ([], [e for e in all_expr if e not in bl_kill])

get_in_out()

b_gen = []
b_kill = []
b_ins = []
b_outs = []

for n in range(1, len(blocks) + 1):
    b_gen.append(gen_kill.get(n)[0])
    b_kill.append(gen_kill.get(n)[1])
    b_ins.append(in_out.get(n)[0])
    b_outs.append(in_out.get(n)[1])


df1 = pd.DataFrame({'gen': b_gen, 'kill': b_kill},
                   index=['B' + str(n) for n in blocks])
df2 = pd.DataFrame({'in': b_ins, 'out': b_outs}, index=[
                   'B' + str(n) for n in blocks])
print('GEN | KILL')
print(df1.to_markdown())

print('\n IN | OUT')
print(df2.to_markdown())
