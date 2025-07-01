from flowpipe.pipeline import PipeLine
from flowpipe.executor import Executor

def test_simple_serial_execution():
    pipe = PipeLine()
    pipe.add_node("a", lambda: 2)
    pipe.add_node("b", lambda: 3)
    pipe.add_node("add", lambda x, y: x + y, dependencies=["a", "b"])

    executor = Executor(pipe)
    result = executor.run(use_threads=False)

    assert result["a"] == 2
    assert result["b"] == 3
    assert result["add"] == 5

def test_simple_threaded_execution():
    pipe = PipeLine()
    pipe.add_node("a", lambda: 4)
    pipe.add_node("b", lambda: 6)
    pipe.add_node("add", lambda x, y: x + y, dependencies=["a", "b"])

    executor = Executor(pipe)
    result = executor.run(use_threads=True)

    assert result["a"] == 4
    assert result["b"] == 6
    assert result["add"] == 10

def test_topological_ordering():
    pipe = PipeLine()
    pipe.add_node("input1", lambda: 1)
    pipe.add_node("input2", lambda: 2)
    pipe.add_node("add", lambda x, y: x + y, dependencies=["input1", "input2"])
    sorted_names = [n.name for n in pipe.get_toposorted_order()]
    
    # Ensure input nodes come before dependent node
    assert sorted_names.index("input1") < sorted_names.index("add")
    assert sorted_names.index("input2") < sorted_names.index("add")

def test_cycle_detection():
    pipe = PipeLine()
    pipe.add_node("a", lambda: 1, dependencies=["b"])
    pipe.add_node("b", lambda: 2, dependencies=["a"])
    
    try:
        pipe.get_toposorted_order()
        assert False, "Expected ValueError for cycle"
    except ValueError as e:
        assert "Cycle detected" in str(e)
