from simplex import Simplex
from LP import LPSolver

def testDegnerateSolver():
    solver = Simplex([0.0, 0.0, 0.0, 3/4, -20.0, 1/2, -6.0, 0.0])
    solver.add_constraint([1, 0, 0, 1/4, -8, -1, 9], 0)
    solver.add_constraint([0, 1, 0, 1/2, -12, -1/2, 3], 0)
    solver.add_constraint([0, 0, 1, 0, 0, 1, 0], 1)
    solver.set_index([1, 2, 3])
    solver.solveStandard(10)
    solver.solveBlandRule(10)
    solver.print_info()


def testLPSolver():
    solver = Simplex([0, 0, 0,-12, 0, -284])
    solver.add_constraint([0, -1, 1, -1, 0], 16)
    solver.add_constraint([1, 2, 0, 1, 0], 12)
    solver.add_constraint([0, 3, 0, 1, 1], 17)
    solver.print_info()
    solver.set_index([3, 1, 5])
    solver.pivot(5, 2)
    solver.print_info()

def testPivot():
    solver = Simplex([0.0, 0.0, 0.0, 1.0, 2.0, 1.0, 1.0])
    solver.add_constraint([1, 0, 0, 1, 1, -1], 5)
    solver.add_constraint([0, 1, 0, 2, -3, 1], 3)
    solver.add_constraint([0, 0, 1, -1, 2, -1], -1)
    solver.set_index([1, 2, 3])
    print(solver.table)
    solver.pivot(1, 4)
    print(solver.table)

def testStandardSolver():
    tester = LPSolver([-4.0, -2.0, 1.0, 0.0, 0.0, 0.0])
    tester.add_line([1, 1, 1, 1, 0, 0], 4)
    tester.add_line([1, -1, -2, 0, 1, 0], 3)
    tester.add_line([3, 2, 1, 0, 0, 1], 12)
    tester.solve()
    tester.solve()
    return

def testShadowPrice():
    tester = LPSolver([-4.0, -2.0, 1.0, 0.0, 0.0, 0.0])
    tester.add_line([1, 1, 1, 1, 0, 0], 4)
    tester.add_line([1, -1, -2, 0, 1, 0], 3)
    tester.add_line([3, 2, 1, 0, 0, 1], 12)
    tester.solve()
    tester.getShadowPrice()

def testWorker():
    k = 2
    p = LPSolver([-2, -7, -5, 0, 0, 0, 0])
    p.add_line([1,1,1,1,0,0,0], k)
    p.add_line([1,0,0,0,1,0,0], 1)
    p.add_line([0,1,0,0,0,1,0], 1)
    p.add_line([0,0,1,0,0,0,1], 1)
    p.solve()
    p.getShadowPrice()


if __name__ == '__main__':
    testLPSolver()
#    testPivot() # passed
#    testLPSolver() # passed
#    testDegnerateSolver() # passed
#    testStandardSolver() # passed
#    testShadowPrice()
