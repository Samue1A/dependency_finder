import ast

# Example Python code with class instantiation
code = """
class MyClass2:
    def _init_(self):
        pass

class MyClass1(MyClass2):
    def _init_(self):
        pass

my_instance = MyClass1(MyClass2())
"""

# Parse the code into an AST
tree = ast.parse(code)

class_names = []
instance_names = []

# Find class names
for node in ast.walk(tree):
    if isinstance(node, ast.ClassDef):
        class_names.append(node.name)

# Find instance names
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        instance_names.append(node.func.id)

print("Class names:", class_names)
print("Instance names:", instance_names)

# Compare class names with instance names
for class_name in class_names:
    for instance_name in instance_names:
        if class_name == instance_name:
            print("Matching class and instance name:", class_name)