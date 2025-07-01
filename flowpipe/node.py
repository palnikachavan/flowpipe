# Features of Node
# 1. Stores the function to run                             Done
# 2. Tracks which other nodes it depends on (by name)       Done
# 3. Accepts inputs dynamically at runtime                  Done
# 4. Caches the result of its execution                     TO DO 

from typing import Callable, List, Any

class Node:

    # constructor for creating an initial blueprint of the node
    def __init__(self, name : str, func : Callable, dependencies : List[str] = None): # type: ignore
        """
        Initialize a Node.

        Args:
            name: Unique identifier of the node.
            func: The function this node wraps.
            dependencies: List of other node names this node depends on.
        """
        self.name = name
        self.func = func
        self.dependencies = dependencies or []
        self.result = None


    def run(self, inputs : List[Any]) -> Any:
        """
        Generate output by executing the function wrapped by the Node

        Args:
            List[Any] inputs: Output from dependent nodes in the correct order.

        Returns:
            Any: The result of the function.
        """
        
        # when we write self.func(*inputs) => it expands the list [inputs] into positional arguments.
        self.result = self.func(*inputs)
        return self.result
