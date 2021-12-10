from typing import List # for annotations

class Edge :

   def __init__(self, arg_src : int, arg_dst : int, arg_weight : int) :
       self.src = arg_src
       self.dst = arg_dst
       self.weight = arg_weight

class Graph :

    def __init__(self, num_nodes : int, edgelist : List[Edge]) :
        self.num_nodes = num_nodes
        self.edgelist  = edgelist
        self.parent    = []
        self.rank      = []
        # mst stores edges of the minimum spanning tree
        self.mst       = []

    def FindParent(self, node : int) :
        # With path-compression.
        if node != self.parent[node] :
            self.parent[node] = self.FindParent(self.parent[node])
        return self.parent[node]

        # Without path compression
        # if node == self.parent[node] :
        #    return node
        # return self.FindParent(self.parent[node])

    def KruskalMST(self):

        self.parent = [None] * self.num_nodes
        self.rank   = [None] * self.num_nodes

        for n in range(self.num_nodes) :
            self.parent[n] = n # Every node is the parent of itself at the beginning
            self.rank[n] = 0   # Rank of every node is 0 at the beginning

        for edge in self.edgelist :
            root1 = self.FindParent(edge.src)
            root2 = self.FindParent(edge.dst)

            # Parents of the source and destination nodes are not in the same subset
            # Add the edge to the spanning tree
            if root1 != root2 :
               self.mst.append(edge)
               if self.rank[root1] < self.rank[root2] :
                  self.parent[root1] = root2
                  self.rank[root2] += 1
               else :
                  self.parent[root2] = root1
                  self.rank[root1] += 1
        return self.mst