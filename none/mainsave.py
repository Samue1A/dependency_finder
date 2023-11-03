import ast
from tree import plot_tree
import  sys
import importlib
from outer import find_outer_used_functions

def find_used_functions(file_path):
    used_functions = {}

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

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef): #or isinstance(node, ast.ClassDef):
            function_name = node.name
            used_functions[function_name] = set()

            for item in ast.walk(node):
                if isinstance(item, ast.Call):
                    try:
                        print('//////////////', item.func.id)
                    except:
                        print('//////////////////', item.func.attr)
                    
                    print(used_functions)
                    if isinstance(item.func, ast.Name):
                        used_functions[function_name].add(item.func.id)
                    elif isinstance(item.func, ast.Attribute) and isinstance(item.func.value, ast.Name):
                        module_name = item.func.value.id
                        if module_name in imported_modules:
                            # try:
                                print('cara messi cara messi')
                                used_functions[function_name].add(
                                    {
                                        f'{module_name}.{item.func.attr}': ('asdf',1,2) #find_outer_used_functions(eval(f"{module_name}.{item.func.attr}"))
                                        }
                                    )
                                print('suuuuuuuu', used_functions[function_name][f'{module_name}.{item.func.attr}'], find_outer_used_functions(f"{module_name}.{item.func.attr}"))
                            # except:
                            #     used_functions[function_name].add(f"{module_name}.{item.func.attr}")
                            
                        else:
                            used_functions[function_name].add(f".{item.func.attr}")

    return used_functions

def print_dict(dict, indent=0):
    for item in dict:
        
        print(('    '*(indent-1) + " '-->" + str(item))*indent or str(item))
        try:
            print_dict(dict[item], indent+1)
        except:
            pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(' Usage: "python main.py <filepath> (tree)"')
    else:
        file_path = sys.argv[1]
        dependdencies = find_used_functions(file_path)
        print(dependdencies)
        print_dict(dependdencies)
        try:
            if sys.argv[2] == 'tree':
                plot_tree(dependdencies)
        except IndexError:
            pass