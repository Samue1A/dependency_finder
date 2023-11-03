import ast

def find_inherited_from_file(file_path, target_name):
    with open(file_path, 'r') as file:
        source_code = file.read()

    tree = ast.parse(source_code)
    inherited_entities = set()
    functioncl_names = []
    argument_names = []

    classmaybe = False

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            functioncl_names.append(node.name)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            argument_names.append(node.func.id)
        if isinstance(node, ast.ClassDef) and node.name == target_name:
            classmaybe = True
            # Found the target class, inspect its base classes and decorators
            for base_node in node.bases:
                if isinstance(base_node, ast.Name):
                    inherited_entities.add(base_node.id)
            for decorator_node in node.decorator_list:
                if isinstance(decorator_node, ast.Name):
                    inherited_entities.add(decorator_node.id)
    if not classmaybe:
        inherited_entities = set()
        functioncl_names = []
        argument_names = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                for arg in node.args:
                    if isinstance(arg, ast.Name):
                        argument_names.append(arg.id)
            if isinstance(node, ast.FunctionDef):
                functioncl_names.append(node.name)
                if node.name == target_name:
                    for child_node in ast.walk(node):
                        if isinstance(child_node, ast.Call):
                            if isinstance(child_node.func, ast.Name) and child_node.func.id in functioncl_names:
                                inherited_entities.add(child_node.func.id)
                for decorator_node in node.decorator_list:
                    if isinstance(decorator_node, ast.Name):
                        inherited_entities.add(decorator_node.id)
    
    print(functioncl_names, argument_names)

    if classmaybe:
        functioncl_names.remove(target_name)

    for func_name in functioncl_names:
        if func_name in argument_names:
            inherited_entities.add(func_name)

            

    return list(inherited_entities)

# Example usage:
file_path = 'none/read_file.py'  # Replace with the path to the target file
target_name = 'num'  # Replace with the name of the class or function you want to inspect

inherited_entities = find_inherited_from_file(file_path, target_name)
print(f"{target_name} inherits from (including base classes and decorators): {inherited_entities}")