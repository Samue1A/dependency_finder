import ast

def find_function_class_references(file_path, target_name):
    references = []

    def visit(node):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == target_name:
                references.append(node.func.id)
        elif isinstance(node, ast.ClassDef):
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == target_name:
                    references.append(node.name)

        for child_node in ast.iter_child_nodes(node):
            visit(child_node)

    with open(file_path, 'r') as file:
        code = file.read()
        tree = ast.parse(code)

    for node in ast.walk(tree):
        visit(node)

    return references

file_path = 'none/read_file.py'
target_name = 'num'
references = find_function_class_references(file_path, target_name)
print(references)