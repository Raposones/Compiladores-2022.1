import pandas as pd

blocks = {}
blocks_use_def = {}
blocks_in_out = {}
block_vertex_aux = -1

def get_use_def(b):
    block_lines = b[0]
    defs = []
    uses = []
    for code_line in block_lines:
        aux = code_line.split(' ')
        if 'return' in aux:
            aux.remove('return')
        if 'if' in aux:
            aux.remove('if')
            aux.remove('goto')
        if len(aux) > 1 and aux[1] == '=' and aux[0] not in defs + uses:
            if aux.count(aux[0]) > 1:
                uses.append(aux[0])
            else:
                defs.append(aux[0])
            for word in aux[2:]:
                if word not in defs + uses and word.isalnum() and not word.isdigit() and 'B' not in word:
                    uses.append(word)
        else:
            for word in aux:
                if word not in defs + uses and word.isalnum() and not word.isdigit() and 'B' not in word:
                    uses.append(word)
    return uses, defs


def get_in_out():
    dict_aux = {}
    global blocks_in_out
    while True:
        for num in range(len(blocks), 0, -1):
            b = blocks.get(num)
            b_next = b[1]
            b_use_def = blocks_use_def.get(num)
            b_def = b_use_def[1]
            b_use = b_use_def[0]
            b_out = []
            for ver in b_next:
                b_out.extend(blocks_in_out.get(int(ver))[0])
            b_out = list(set(b_out))
            b_in = list(
                set(b_use + [var for var in b_out if var not in b_def]))
            dict_aux[num] = (b_in, b_out)
        if dict_aux == blocks_in_out:
            break
        blocks_in_out = dict_aux

f = open('input.txt', 'r')
while True:
    block = []
    line = f.readline()
    if line == '':
        break
    line = line.split(' ')
    block_num = int(line[0])
    block_lines = int(line[1])
    for i in range(block_lines + 1):
        aux = next(f).rstrip(' \n')
        if i == block_lines:
            ver = aux.split(' ')
            ver = [int(x) for x in ver]
            if ver == [0]:
                ver = [1]
        else:
            block.append(aux)
    blocks[block_num] = (block, ver)

for n in range(1, len(blocks) + 1):
    block = blocks.get(n)
    blocks_in_out[n] = ([], [])
    blocks_use_def[n] = get_use_def(block)

get_in_out()

b_defs = []
b_uses = []
b_ins = []
b_outs = []

for n in range(1, len(blocks) + 1):
    b_defs.append(blocks_use_def.get(n)[1])
    b_uses.append(blocks_use_def.get(n)[0])
    b_ins.append(blocks_in_out.get(n)[0])
    b_outs.append(blocks_in_out.get(n)[1])

df = pd.DataFrame({'def': b_defs, 'use': b_uses, 'in': b_ins,
                  'out': b_outs}, index=['B' + str(n) for n in blocks])
print(df.to_markdown())
