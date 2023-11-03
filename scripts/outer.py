import ast
import inspect

import math

def find_outer_used_functions(target_function):
    used_functions = set()
    stack = [target_function]

    while stack:
        func = stack.pop()
        source = inspect.getsource(func)
        tree = ast.parse(source)
        

        #------------------------------------------
        #finding dem moduuuuuuuuuuuules
        imported_modules = set()
        filePath = inspect.getfile(func)
        with open(filePath, 'r') as file:
            fileTree = ast.parse(file.read())
        for node in ast.walk(ast.parse(fileTree)):
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
        #------------------------------------


        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    used_functions.add(node.func.id)
            elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                module_name = node.value.id
                if module_name in imported_modules:
                    used_functions.add(f"{module_name}.{node.attr}")
                else:
                    used_functions.add(f".{node.attr}")


    return used_functions


# used_functions = find_used_functions(math.sqrt)
