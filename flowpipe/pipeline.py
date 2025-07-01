# Features
# Store all nodes
# Validate and register them
# Sort them topologically (respecting dependencies)

from .node import Node
from typing import Dict, List, Callable, Optional

class PipeLine:
    def __init__(self) -> None:
        # initialize a map of name of node to pointer of node
        self.nodes: Dict[str, Node] = {}

    def add_node(self, name : str, func : Callable, dependencies : List[str] = None): # type: ignore
        """
        Adds a new node to the pipeline

        Args:
            name (str): Unique name for the node.
            func (Callable): Callable function.
            dependancies (List[str], optional): Names of nodes this one depends on. Defaults to None.
        """
        if name in self.nodes:
            raise ValueError(f"Node '{name}' already exists.")
        self.nodes[name] = Node(name, func, dependencies)

    def get_node(self, name: str) -> Optional[Node]:
        """
        Returns the node with the given name.
        Raises an error if the node does not exist.
        """
        node = self.nodes.get(name)
        if node is None:
            raise ValueError(f"Node '{name}' not found.")
        return node

    def get_toposorted_order(self) -> List[Node]:
        """
        Returns a list of nodes sorted topologically.
        Raises error if cycle detected.
        """
        visited = set()
        temp_mark = set()
        sorted_nodes = []

        def visit(n: str):
            if n in temp_mark:
                raise ValueError(f"Cycle detected at node: {n}")
            if n not in visited:
                temp_mark.add(n)
                node = self.get_node(n)
                if node is None:
                    raise ValueError(f"Node '{n}' not found in the pipeline.")
                for dep in node.dependencies:
                    visit(dep)
                temp_mark.remove(n)
                visited.add(n)
                sorted_nodes.append(node)

        for node_name in self.nodes:
            visit(node_name)

        return sorted_nodes