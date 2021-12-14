class UF:
    """ Code from http://python-algorithms.readthedocs.org/en/latest/_modules/python_algorithms/basic/union_find.html """

    def __init__(self, N):
        self._id = list(range(N))
        self._count = N
        self._rank = [0] * N
        self._N = N
        self._symbol_to_index = {}
        self._index_to_symbol = {}

    def find(self, p):
        if isinstance(p, int) and p < self._N and            p not in self._index_to_symbol:
            self._symbol_to_index[p] = p
            self._index_to_symbol[p] = p
        else:
            self._symbol_to_index.setdefault(p, len(self._symbol_to_index))
            self._index_to_symbol.setdefault(self._symbol_to_index[p], p)
        i = self._symbol_to_index[p]
        if i >= self._N:
            raise IndexError('You have been exceeding the UF capacity')

        id = self._id
        while i != id[i]:
            id[i] = id[id[i]]
            i = id[i]
        return i


    def union(self, p, q):

        id = self._id
        rank = self._rank

        i = self.find(p)
        j = self.find(q)
        if i == j:
            return

        self._count -= 1
        if rank[i] < rank[j]:
            id[i] = j
        elif rank[i] > rank[j]:
            id[j] = i
        else:
            id[j] = i
            rank[i] += 1