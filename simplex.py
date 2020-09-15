import numpy as np
import fractions

'''
We assume: • # of variables = n ≥ m = # of equations (otherwise, the system Ax = b is overdetermined);
• rows of A are linearly independent (otherwise, the constraints are redundant or inconsistent).
• ⇒ rank(A) = m
Input is formalized.
'''

eps = 1e-6
inf = 1e50
max_decimals = -1 #-1 as a/b, val>=0 as round.
original_options = None

# change the output of numpy
def DivSwitch(flag):
    global original_options
    if flag == True:
        original_options = np.get_printoptions()
        np.set_printoptions(formatter={'all': lambda x: str(fractions.Fraction(x).limit_denominator())})
    else:
        np.set_printoptions(**original_options)
    return

class Simplex():
    # x0 + obj[:-1]^T x = obj[-1]
    def __init__(self, obj):
        self.table = np.array([[1] + obj]).astype(np.float)
        self.index = []
        self.map_index = [0] * len(obj)
        self.step = 0

    # print the information recorded in tableu.
    def print_info(self):
        print("<----- step : %d ----->" % self.step)
        self.step += 1
        print("The basic index set is ", self.index[1:])
        if max_decimals >= 0:
            print("Tableu\n", np.around(self.table, decimals=max_decimals))
        else:
            DivSwitch(True)
            print("Tableu\n", self.table)
            DivSwitch(False)
        return

    # set the basic index set to a.
    def set_index(self, a):
        a = [0] + a
        i = 0
        self.index = []
        self.map_index = [-1] * (self.table.shape[1]-1)
        for x in a:
            self.index.append(x)
            self.map_index[x] = i
            i += 1
        return

    # add one equal constraint a x = b.
    def add_constraint(self, a, b):
        self.table = np.vstack([self.table, [0] + a + [b]])
        return

    # pivot: add q into index set, and remove p.
    def pivot(self, p, q):
        m, n = self.table.shape
        i = self.map_index[p]
        assert i != -1
        if np.abs(self.table[i, q]) <= eps:
            print("Error: the pivot of %d, %d is impossible!\n" % (p, q))
            return False
        if np.abs(self.table[i, -1]) <= eps:
            print("Warning: It is a degenerate step!")
        self.table[i] /= self.table[i, q]
        for j in range(m):
            if j != i and self.table[j, q]:
                self.table[j] -= self.table[i] * self.table[j, q]
        self.map_index[p] = -1
        self.map_index[q] = i
        self.index[i] = q
        return True

    # check if the LP is unbounded.
    def check_no_limit(self):
        _, n = self.table.shape
        for i in range(1, n-1):
            if self.table[0, i] > eps:
                bound = max(self.table[:,i])
                if bound <= eps:
                    return True
        return False

    # solve simplex with standard way.
    def solveStandard(self, max_step = 1000):
        m, n = self.table.shape
        val = max(self.table[0, 1:-1])
        self.step = 0
        while val > 0 and self.step < max_step:
            self.print_info()
            if self.check_no_limit():
                print("The problem is unbounded!\n")
                return
            q = np.argmax(self.table[0, 1:-1]) + 1
            bound = self.table[1:,-1] / (self.table[1:,q] + eps)
            bound[self.table[1:,q] <= eps] = inf
            p = np.argmin(bound) + 1
            p = self.index[p]
            print("<----- pivoting %d, %d ----->\n" % (p,q))
            self.pivot(p, q)
            val = max(self.table[0, 1:-1])

    # solve simplex with bland's rule
    def solveBlandRule(self, max_step = 1000): #solve simplex with bland's rule
        m, n = self.table.shape
        val = max(self.table[0, 1:-1])
        self.print_info()
        self.step = 0
        while val > 0 and self.step < max_step:
            self.print_info()
            if self.check_no_limit():
                print("The problem is unbounded!\n")
                return
            q = 0
            for i in range(1, n-1):
                if self.table[0, i] > eps:
                    q = i
                    break
            bound = self.table[1:,-1] / (self.table[1:,q] + eps)
            bound[self.table[1:,q] <= eps] = inf
            p = np.argmin(bound) + 1
            p = self.index[p]
            print("<----- pivoting %d, %d ------>\n" % (p,q))
            self.pivot(p, q)
            val = max(self.table[0, 1:-1])
        return
