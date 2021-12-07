from PIL import Image
import numpy as np
from utils.disjoint_set_forest import DisjointSet
from utils.graph import Graph

example_img = np.array([[1, 2, 3],
                        [4, 5, 6],
                        [7, 8, 9]]) # TODO: Change to input image post-testing

G = Graph(example_img)
V, E = G.adjacency_matrix()

# Sort E into π = (o1,...,om), by non-decreasing edge weight.
E = sorted(E, key=lambda x: x[2])

# Start with a segmentation S^0, where each vertex v_i is in its own component.
segmentation = DisjointSet(example_img.size)
def mint(c_1, c_2):
    """Compute minimum internal difference"""
    pass
# Construct S^q given S^{q−1} as follows. Let v_i and v_j denote the vertices connected by the q-th edge in the ordering, i.e., o_q = (v_i,v_j). If vi and v_j are in disjoint components of S+{q−1} and w(o_q) is small compared to the internal difference of both those components, then merge the two components otherwise do nothing.
for q in E:
    v_i, v_j, weight = q[0], q[1], q[2]
    a = segmentation.find(v_i)
    b = segmentation.find(v_j)
    if a != b and weight <= mint(a, b):
        segmentation.join(a, b)
