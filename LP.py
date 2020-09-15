import simplex
import numpy as np

class LPSolver(simplex.Simplex):
    def __init__(self, cT):
        obj = list(cT * -1) + [0]
        super().__init__(obj)
        self.cT = np.array(cT)
        self.A = None
        self.b = []

    def add_line(self, a, b):
        if self.A is None:
            self.A = np.array(a)
        else:
            self.A = np.vstack([self.A, a])
        self.b = np.append(self.b, b)

    def initBasicSet(self):
        m, n = self.A.shape
        auxiliary = simplex.Simplex(list(np.sum(self.A,axis=0)) + [0]*m + [sum(self.b)])
        MI = [0]*m
        for i in range(m):
            MI[i] = 1
            auxiliary.add_constraint(list(self.A[i]) + MI, self.b[i])
            MI[i] = 0
        auxiliary.set_index(list(range(n+1, n+m+1)))
        print("<----- Begin The Auxiliary LP ----->")
        auxiliary.solveStandard(10)
        auxiliary.print_info()
        print("<----- Finish The Auxiliary LP ----->")

        obj = auxiliary.table[0, -1]
        if obj > simplex.eps:
            print("It is not feasible!")
        else:
            j = 1
            for i in range(m):
                if auxiliary.index[i] > n:
                    while auxiliary.map_index[j]: j += 1
                    auxiliary.pivot(auxiliary.index[i], j)
            self.table = np.hstack((auxiliary.table[:,:n+1], auxiliary.table[:,-1:]))
            self.table[0] = np.array([[1] + list(self.cT * -1) + [0.0]]).astype(np.float)
            self.set_index(auxiliary.index[1:])
            for i in range(1, n):
                if self.map_index[i] > 0:
                    self.table[0] -= self.table[self.map_index[i]] * self.table[0, i]

        return

    def solve(self):
        self.initBasicSet()
        self.solveStandard(10)
        self.print_info()

    # please call self.solve first
    def getShadowPrice(self):
        print("\n<----- Printing the factors in shadowprices ----->")
        simplex.DivSwitch(True)
        mp = np.array(self.map_index)
        B = self.A[:, mp[1:] > 0]
        print("B = \n", B)
        cB = self.cT[mp[1:] > 0].T
        print("cB = \n", cB)
        B = np.matrix(B).astype(np.float)
        print("B^{-1} = \n", B.I)
        Pi = np.matmul((B.I).T, cB)
        print("Pi = \n", Pi)
        simplex.DivSwitch(False)
        print("\n<----- Printing over ----->")
        return Pi