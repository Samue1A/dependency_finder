def recurr(tree, indLines, indx=[]):
    if indLines[0]==len(lines):
        return tree

    

    i = indLines[0]
    for i in range(indLines[0], indLines[1]):
        if list(lines[i].lstrip())[0:3] == ['d', 'e', 'f'] or list(lines[i].lstrip())[0:5] == ['c', 'l', 'a', 's', 's']:


            mod(tree, indx, lines[i].lstrip().split(' ')[1], {
                'type': (list(lines[i].lstrip())[0:3] == ['d', 'e', 'f'])*'func' or 'class',
                'lines': [i+1, nLines(i+1, lines)],
                'children': {}
            })
            indx.append(lines[i].lstrip().split(' ')[1])
            indx.append('children')
            return recurr(tree,
                   [i+1, nLines(i+1, lines)],
                   indx
                   )

    try:
        indx.pop()
        indx.pop()
    except:
        pass
    return recurr(tree, [i+1, nLines(i+1, lines)],
                   indx
                   )
    


def nLines(current, text):
    l = current
    while l < len(text) and len(text[l]) - len(text[l].lstrip()) >= len(text[current]) - len(text[current].lstrip()):
        l += 1
    return l

def mod(bob, inds, new, change, ind=0):
    if not inds or len(inds) == ind or not isinstance(bob[inds[ind]], dict):
        bob[new] = change
    else:
        mod(bob[inds[ind]], inds, new,change, ind+1)




with open('no_run.py', 'r') as f:
    lines = [line.replace('\n', '') for line in f]
    try:
        while True:
            lines.remove('')
    except:
        pass
    tree = {}
    print(recurr(tree, [0, len(lines)]))

# with open('no_run.py') as f:
#     lines = [line.replace('\n', '') for line in f]
#     try:
#         while True:
#             lines.remove('')
#     except:
#         pass
#     print(lines)
#     funcs_cls = {}
#     for i in range(len(lines)):
#         print(list(lines[i])[0:2])
#         if list(lines[i])[0:3] == ['d', 'e', 'f'] or list(lines[i])[0:5] == ['c', 'l', 'a', 's', 's']:

#             i+=1
#             while lines[i][0] == ' ' and lines[i][1] == ' ':
#                 i += 1
#                 funcs_cls.append(lines[i])

# print(funcs_cls)
