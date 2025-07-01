# Purpose of the Executor
# Accept a Pipeline instance
# Execute all nodes in topological order
# If use_threads=True, run independent nodes in parallel

# flowpipe/executor.py

from .pipeline import PipeLine
from .node import Node
from typing import Dict, Any
from threading import Thread
from time import sleep

class Executor:
    def __init__(self, pipeline: PipeLine):
        self.pipeline = pipeline
        self.results: Dict[str, Any] = {}

    def run(self, use_threads: bool = False) -> Dict[str, Any]:
        """
        Executes the pipeline.

        :param use_threads: If True, uses threads for parallel execution.
        :return: A dictionary of node_name -> result.
        """
        if use_threads:
            print("[flowpipe] Running pipeline in threaded mode.")
            return self._run_threaded()
        else:
            print("[flowpipe] Running pipeline in serial mode.")
            return self._run_serial()

    def _run_serial(self) -> Dict[str, Any]:
        """
        Runs the pipeline serially (one node at a time).
        """
        for node in self.pipeline.get_toposorted_order():
            inputs = [self.results[dep] for dep in node.dependencies]
            print(f"[flowpipe] Running node: {node.name} (Serial)")
            self.results[node.name] = node.run(inputs)
        return self.results

    def _run_threaded(self) -> Dict[str, Any]:
        """
        Runs the pipeline using threads (parallel when possible).
        """
        import threading

        sorted_nodes = self.pipeline.get_toposorted_order()
        in_progress: Dict[str, Thread] = {}
        completed = set()

        def run_node(node: Node):
            print(f"[flowpipe] Running node: {node.name} (Threaded)")
            inputs = [self.results[dep] for dep in node.dependencies]
            result = node.run(inputs)
            self.results[node.name] = result
            completed.add(node.name)

        while len(completed) < len(sorted_nodes):
            for node in sorted_nodes:
                if node.name in completed or node.name in in_progress:
                    continue
                if all(dep in completed for dep in node.dependencies):
                    thread = threading.Thread(target=run_node, args=(node,))
                    thread.start()
                    in_progress[node.name] = thread

            # Clean up finished threads
            for name, thread in list(in_progress.items()):
                if not thread.is_alive():
                    thread.join()
                    del in_progress[name]

            sleep(0.01)  # Prevents CPU hogging loop

        return self.results
