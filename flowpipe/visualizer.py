from .pipeline import PipeLine
import json 

def visualize_pipeline(pipeline: PipeLine, output_file: str = None, view: bool = True, engine: str = "graphviz"): # type: ignore
    """
    Visualizes the pipeline DAG.

    pipeline: Pipeline instance.
    output_file: If provided, saves image to file.
    view: If True, shows the graph.
    engine: "graphviz" or "networkx"
    """
    if engine == "graphviz":
        try:
            _visualize_with_graphviz(pipeline, output_file, view)
        except Exception as e:
            print(f"[flowpipe] Graphviz failed: {e}. Falling back to networkx.")
            _visualize_with_networkx(pipeline, output_file, view)
    else:
        _visualize_with_networkx(pipeline, output_file, view)

def _visualize_with_graphviz(pipeline: PipeLine, output_file: str, view: bool):
    from graphviz import Digraph

    dot = Digraph(comment="Flowpipe Pipeline", format='png')
    dot.attr(rankdir='LR')

    for name, node in pipeline.nodes.items():
        dot.node(name, label=name, shape='box')
        for dep in node.dependencies:
            dot.edge(dep, name)

    if output_file:
        path = dot.render(output_file, view=view)
        print(f"[flowpipe] Saved DAG graph to: {path}")
    else:
        print(dot.source)

def _visualize_with_networkx(pipeline: PipeLine, output_file: str, view: bool):
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.DiGraph()
    G.add_nodes_from(pipeline.nodes.keys())

    for name, node in pipeline.nodes.items():
        for dep in node.dependencies:
            G.add_edge(dep, name)

    pos = nx.spring_layout(G)

    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=12, arrows=True, edge_color='gray')

    if output_file:
        plt.savefig(output_file)
        print(f"[flowpipe] Saved DAG graph to: {output_file}")
    if view:
        plt.show()
    plt.close()

def export_PipeLine_as_JSON(pipeline : PipeLine, output_file : str = None) -> dict: # type: ignore
    """
    Exports pipeline DAG as a D3-compatible JSON structure.

    Args:
        pipeline (PipeLine): Pipeline instance.
        output_file (str, optional):  If provided, saves JSON to file. Defaults to None.

    Returns:
        dict:  Dictionary with 'nodes' and 'links'.
    """
    
    data  = {
        "nodes": [],
        "links": []
    }
    
    for name, node in pipeline.nodes.items():
        data['nodes'].append({'id':name})
        for dep in node.dependencies:
            data['links'].append({'source':dep, 'target': name})
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(data, f, indent = 2)
        print(f"[flowpipe] DAG exported as D3 JSON to {output_file}")
    return data