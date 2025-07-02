from flowpipe.pipeline import PipeLine
from flowpipe.executor import Executor
from flowpipe.visualizer import visualize_pipeline, export_PipeLine_as_JSON
import time

# Step functions
def input1():
    time.sleep(1)  # simulate delay
    return 2

def input2():
    time.sleep(1)
    return 3

def add(x, y):
    return x + y

def square(x):
    return x * x

def double(x):
    return 2 * x

# Build pipeline
pipe = PipeLine()
pipe.add_node("input1", input1)
pipe.add_node("input2", input2)
pipe.add_node("sum", add, dependencies=["input1", "input2"])
pipe.add_node("double_sum", double, dependencies=["sum"])
pipe.add_node("square_sum", square, dependencies=["sum"])

# Run serially
print("\n--- Running Serial Execution ---")
serial_executor = Executor(pipe)

start_serial = time.perf_counter()
serial_result = serial_executor.run(use_threads=False)
end_serial = time.perf_counter()

print("Serial Results:", serial_result)
print(f"Time taken (serial): {end_serial - start_serial:.2f} seconds")

# Build pipeline again (fresh nodes)
pipe = PipeLine()
pipe.add_node("input1", input1)
pipe.add_node("input2", input2)
pipe.add_node("sum", add, dependencies=["input1", "input2"])
pipe.add_node("double_sum", double, dependencies=["sum"])
pipe.add_node("square_sum", square, dependencies=["sum"])

# Run threaded
print("\n--- Running Threaded Execution ---")
threaded_executor = Executor(pipe)

start_threaded = time.perf_counter()
threaded_result = threaded_executor.run(use_threads=True)
end_threaded = time.perf_counter()

print("Threaded Results:", threaded_result)
print(f"Time taken (threaded): {end_threaded - start_threaded:.2f} seconds")


# visualize using graphviz
# visualize_pipeline(pipe, output_file="example_dag.png", engine="graphviz", view=True)

# visualize using networkx and matplotlib
visualize_pipeline(pipe, output_file="example1_dag.png", engine="networkx", view=True)

export_PipeLine_as_JSON(pipe, output_file="example_dag.json")