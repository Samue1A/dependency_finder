import networkx as nx
import matplotlib.pyplot as plt


def build_tree(graph, parent, data, parent_label=""):
    for key, value in data.items():
        current_label = (f"{parent_label}/{key}" if parent_label else key)
        
        if parent is not None:
            graph.add_node(current_label )
            graph.add_edge(parent, current_label)
        if isinstance(value, dict):
            build_tree(graph, current_label, value, current_label)
        elif isinstance(value, set):
            for item in value:
                graph.add_node(f'{key}/{item}')
                graph.add_edge(key, f'{key}/{item}')

            
def plot_tree(data): 
    graph = nx.DiGraph() 
    root = "Root"
    graph.add_node(root)
    build_tree(graph, root, data, "")

    pos = nx.spring_layout(graph)
    labels = {node: node.split("/")[-1] for node in graph.nodes()}
              
    plt.figure(figsize=(10, 10))
    nx.draw(graph, pos, labels=labels, with_labels=True, node_size=1000, node_color='lightblue', font_size=10, font_color='black')
    plt.axis('off')
    plt.show()
    
    # Example input dictionary

