from flowpipe.node import Node

def myAdd(a : int, b : int):
    return a + b

node = Node("first", myAdd, ['a', 'b'])
print(node.run([2,3]))   # prints 5


node1 = Node("first", myAdd)
print(node1.run([2,3]))   # prints 5