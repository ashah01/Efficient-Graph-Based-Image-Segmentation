from PIL import Image, ImageFilter
from matplotlib.pyplot import *
from collections import defaultdict
import numpy as np
from utils.disjoint_set_forest import UF

def to_graph(im):
    """
    Convert image to graph. 8-connected, based on intensity absolute difference
    """
    
    edges = {}
    num_rows, num_cols = im.height, im.width    
    image = np.empty((num_rows,num_cols, 3))
    
    imiter = iter(im.getdata())
    
    for row in range(num_rows):
        for col in range(num_cols):
            image[row, col, :] = imiter.__next__()

    for row in range(num_rows):
        for col in range(num_cols):
            cur = image[row,col]
            diff = lambda a,b: (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2
            if row < image.shape[0] -1:
                edges[((row,col),(row+1,col))] = diff(cur, image[row+1,col])
            if col < image.shape[1] - 1:
                edges[((row,col), (row, col+1))] = diff(cur, image[row,col+1])
    return edges


def tao(size, k=5000.):
    return k/size

def segment(image, k=5000.):
    uf_nodes = UF(image.width*image.height)
    internal = defaultdict(lambda: (0,1))
    count = 0
    graph = to_graph(image)
    edges = sorted(graph.items(), key=lambda x: x[1])
    for edge in edges:
        count += 1
        to_node = edge[0][1]
        from_node = edge[0][0]
        weight = edge[1]
        
        # set_name is a single node
        set_name1 = uf_nodes.find(to_node)
        set_name2 = uf_nodes.find(from_node)

        int1,size1 = internal[set_name1]
            
        int2,size2 = internal[set_name2]
            
        if weight <= min(int1+tao(size1, k=k), int2+tao(size2,k=k)) and set_name1 != set_name2:
            uf_nodes.union(to_node, from_node)
            new_set_name = uf_nodes.find(to_node)
            del internal[set_name1]
            del internal[set_name2]
            internal[new_set_name] = weight, size1+size2+1
    return uf_nodes


def create_segment_image(union_find, im):
    uf = union_find
    image = np.empty((im.height,im.width), dtype=np.uint16)
    for i in range(im.height):
        for j in range(im.width):
            image[i,j] = uf.find((i,j))
    return image



if __name__ == '__main__':
    image = Image.open('./52.png').filter(ImageFilter.MedianFilter)
    image.thumbnail((28,28))
    imshow(create_segment_image(segment(image, 1000), image), cmap='Accent')
    show()