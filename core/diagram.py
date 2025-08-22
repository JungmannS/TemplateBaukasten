import matplotlib.pyplot as plt
import networkx as nx

def show_tree(user_problem, blocks):
    """Zeigt ein graphisches Baumdiagramm für den Projektpfad."""
    G = nx.DiGraph()
    root = f"Problem: {user_problem}"
    G.add_node(root)

    ebenen = set(b['ebene'] for b in blocks)
    for ebene in ebenen:
        G.add_node(ebene)
        G.add_edge(root, ebene)

    for b in blocks:
        node_label = f"[{b['action']}] {'*'*b['priority']}: {b['text']}"
        G.add_node(node_label)
        G.add_edge(b['ebene'], node_label)

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=3000, font_size=9, arrows=True)
    plt.title("Projektpfad-Diagramm")
    plt.show()