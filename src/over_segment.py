from PIL import Image
import numpy as np
from utils.graph import Graph

example_img = np.array([[1, 2, 3],
                        [4, 5, 6],
                        [7, 8, 9]]) # TODO: Change to input image post-testing

G = Graph(example_img)
V, E = G.adjacency_matrix()

# Sort E into π = (o1,...,om), by non-decreasing edge weight.
E = sorted(E, key=lambda x: x[2])

# Start with a segmentation S^0, where each vertex v_i is in its own component.
