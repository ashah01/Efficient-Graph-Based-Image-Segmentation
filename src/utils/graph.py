import numpy as np

class Graph:
    """Convert image to be segmented into a graph"""
    def __init__(self, image):
        self.image = image

    def _adjacent_pixels(self, pixel_cord):
        x = pixel_cord[0]
        y = pixel_cord[1]
        cord_matrix = [[max(0, x - 1), max(0, y - 1)], [max(0, x - 1), y], [max(0, x - 1), min(self.image.shape[1] - 1, y + 1)],
                        [x, max(0, y - 1)], [x, min(self.image.shape[1] - 1, y + 1)],
                        [min(self.image.shape[0] - 1, x + 1), max(0, y - 1)], [min(self.image.shape[0] - 1, x + 1), y], [min(self.image.shape[0] - 1, x + 1), min(self.image.shape[1] - 1, y + 1)]]
        cord_matrix = np.array(cord_matrix)
        dtype1 = np.dtype((np.void, cord_matrix.dtype.itemsize * np.prod(cord_matrix.shape[1:])))
        b = np.ascontiguousarray(cord_matrix.reshape(cord_matrix.shape[0],-1)).view(dtype1)
        new_arr = []
        for (i, j) in cord_matrix[np.unique(b, return_index=1)[1]]:
            if (i, j) != (x, y):
                new_arr.append([i, j])
        return new_arr

    def _similarity(self, adjacent):
        graph = adjacent
        edges = []
        for key, val in graph.items():
            minuend = self.image[key]
            for i, edge in enumerate(val):
                difference = abs(minuend - self.image[edge[0]][edge[1]])
                graph[key][i] = [edge, difference]
                edges.append([list(key), edge, difference])
        
        return list(map(lambda x: self.image[x], graph.keys())), sorted(list(map(lambda x: [self.image[x[0][0]][x[0][1]], self.image[x[1][0]][x[1][1]], x[2]], edges)), key=lambda x: x[2])

    def adjacency_matrix(self):
        """Outputs adjacency matrix representation of graph."""
        M = {}
        for i, row in enumerate(self.image):
            for j, value in enumerate(row):
                M[i, j] = self._adjacent_pixels([i, j])
        for key, val in M.items():
            for edge in val:
                if list(key) in M[tuple(edge)]:
                    M[tuple(edge)].remove(list(key))
        return self._similarity(M)