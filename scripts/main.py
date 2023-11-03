import ast
from tree import plot_tree
import  sys
import importlib
from outer import find_outer_used_functions

def find_used_functions(file_path, imported_modules):
    used_functions = {}
    
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef): #or isinstance(node, ast.ClassDef):
            function_name = node.name
            used_functions[function_name] = set()

            for item in ast.walk(node):
                if isinstance(item, ast.Call):
                    if isinstance(item.func, ast.Name):
                        used_functions[function_name].add(item.func.id)
                    elif isinstance(item.func, ast.Attribute) and isinstance(item.func.value, ast.Name):
                        module_name = item.func.value.id
                        if module_name in imported_modules:
                            used_functions[function_name].add(f"{module_name}.{item.func.attr}")
                        else:
                            used_functions[function_name].add(f".{item.func.attr}")

    return used_functions




def goDeeper(data, modules, maxDepth):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, set):
                data[key] = nextLayer(list(value), modules, maxDepth)
            elif isinstance(value, dict) or isinstance(value, list):
                goDeeper(value, modules, maxDepth)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, set):
                data[i] = nextLayer(list(item), modules, maxDepth)
                        
            elif isinstance(item, dict) or isinstance(item, list):
                goDeeper(item, modules, maxDepth)
    return data



def nextLayer(data, modules, maxDepth, depth=3):
    m = '.'.join(modules).split('.')
    returnn = []

    for func in data:
        if depth < maxDepth:
            funcName = ('.'.join(func.split('.')[1:]) if '.' in func else func) if len(func[1:].split('.')) == 1 else func.split('.')[-1]
            moduleName = (m[m.index(funcName)-1] if funcName in modules else '') if len(func[1:].split('.')) == 1 else '.'.join(func.split('.')[:-1])

            if len(func[1:].split('.')) > 1 or moduleName in modules:
                returnn.append({funcName: nextLayer([funcName], modules, maxDepth, depth + 1)})
            else:
                try:
                    l = list(find_outer_used_functions(eval(f'{moduleName}.{funcName}' if len(func[1:].split('.')) > 1 else funcName)))
                    returnn.append({funcName: nextLayer(l, modules, maxDepth, depth+1 if funcName not in l else maxDepth+1)})
                except:
                    returnn.append(func)
        else:
            returnn.append(func)



    return returnn



def find_modules(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    # Collect imported modules
    imported_modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_modules.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if node.module:
                    module_name = f"{node.module}.{alias.name}"
                else:
                    module_name = alias.name
                imported_modules.add(module_name)
    
    return imported_modules


def print_tree(data, level=0):
    if isinstance(data, dict):
        if not ( len(data) == 1 and data[str(data.keys()).split("dict_keys(['")[-1].split("'])")[0]][0] == str(data.keys()).split("dict_keys(['")[-1].split("'])")[0] ):
            for key, value in data.items():
                print(('          ' * (level-1) + "       '--->  " + f'{key}:') if level else f'{key}:' or f'{key}:')
                print_tree(value, level + 1)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                print_tree(item, level)
            else:
                print(('          ' * (level-1) + "       '--->  " + str(item)))



if __name__ == "__main__":
    correctInput = True
    if len(sys.argv) < 2:
        print('\nFor correct usage, call the file by entering the following command:\n\n "python main.py <filepath> (depth - int) (tree)"')
        print('\nboth tree and depth are not necessay, their defaults are 4 and no tree respectively; you can call tree without specifying a depth, simply make sure tree is the last arg')
    else:
        file_path = sys.argv[1]
        modules = find_modules(file_path)
        try:
            maxDepth = int(sys.argv[2])
            if maxDepth < 2:
                print('you stinky bozo the minimum depth is 2')
                correctInput = False

        except:
            maxDepth = 3

        if not correctInput:
            exit()

        dependdencies = goDeeper(find_used_functions(file_path, modules), modules, maxDepth)

        
        print_tree(dependdencies)
        print(dependdencies)
        try:
            if sys.argv[-1] == 'tree':
                plot_tree(dependdencies)
        except IndexError:
            pass
