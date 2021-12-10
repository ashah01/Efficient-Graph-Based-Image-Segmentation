from PIL import Image
import numpy as np
from utils import *

example_img = np.arange(9).reshape((3, 3)) # TODO: Change to input image post-testing

def adjacent_pixels(pixel_cord):
    x = pixel_cord[0]
    y = pixel_cord[1]
    cord_matrix = [[max(0, x - 1), max(0, y - 1)], [max(0, x - 1), y], [max(0, x - 1), min(example_img.shape[1] - 1, y + 1)],
                    [x, max(0, y - 1)], [x, min(example_img.shape[1] - 1, y + 1)],
                    [min(example_img.shape[0] - 1, x + 1), max(0, y - 1)], [min(example_img.shape[0] - 1, x + 1), y], [min(example_img.shape[0] - 1, x + 1), min(example_img.shape[1] - 1, y + 1)]]
    cord_matrix = np.array(cord_matrix)
    dtype1 = np.dtype((np.void, cord_matrix.dtype.itemsize * np.prod(cord_matrix.shape[1:])))
    b = np.ascontiguousarray(cord_matrix.reshape(cord_matrix.shape[0],-1)).view(dtype1)
    new_arr = []
    for (i, j) in cord_matrix[np.unique(b, return_index=1)[1]]:
        if (i, j) != (x, y):
            new_arr.append([i, j])
    return new_arr

def similarity(adjacent):
    graph = adjacent
    edges = []
    for key, val in graph.items():
        minuend = example_img[key]
        for i, edge in enumerate(val):
            difference = abs(minuend - example_img[edge[0]][edge[1]])
            graph[key][i] = [edge, difference]
            edges.append([list(key), edge, difference])
    
    return list(map(lambda x: example_img[x], graph.keys())), sorted(list(map(lambda x: [example_img[x[0][0]][x[0][1]], example_img[x[1][0]][x[1][1]], x[2]], edges)), key=lambda x: x[2])

def adjacency_matrix():
    """Outputs adjacency matrix representation of graph."""
    M = {}
    for i, row in enumerate(example_img):
        for j, value in enumerate(row):
            M[i, j] = adjacent_pixels([i, j])
    for key, val in M.items():
        for edge in val:
            if list(key) in M[tuple(edge)]:
                M[tuple(edge)].remove(list(key))
    return similarity(M)

V, E = adjacency_matrix()

segmentation = DisjSet(len(V))

def int(c):
    vertices = [i for i, v in enumerate(segmentation.parent) if v == c]
    dict_map = {vertex:counter for counter, vertex in enumerate(vertices)}
    edges = [Edge(dict_map[edge[0]], dict_map[edge[1]], edge[2]) for edge in E if edge[0] in vertices and edge[1] in vertices]
    mst = Graph(len(vertices), edges)
    return max([el.weight for el in mst.KruskalMST()]) if mst.KruskalMST() else 0

def mint(c1, c2, k=50):
    return min(int(c1) + k/segmentation.size_of(c1), int(c2) + k/segmentation.size_of(c2))

for q in E:
    v_i, v_j, weight = q
    a = segmentation.find(v_i)
    b = segmentation.find(v_j)
    if a != b and weight <= mint(a, b):
        segmentation.merge(a, b)
