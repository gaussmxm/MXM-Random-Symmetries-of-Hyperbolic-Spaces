# Partial implementation of the algorithm in "An Algorithm for 2-Generator
# Fuchsian Groups" by J. Gilman and B. Maskit (doi:10.1307/mmj/1029004258).

# The algorithm takes as input two entries of SL(2,Z) and decides whether or
# not the subgroup of PSL(2,Z) that they generate is non-elementary, free, and
# discrete.

#### Imports ####

import math
import sys

#### Common Methods ####

def determinant(m):
    return (m[0] * m[3]) - (m[1] * m[2])

def negate(m):
    return [-m[0], -m[1], -m[2], -m[3]]

def trace(m):
    return m[0] + m[3]

def T(m):
    return trace(m) / math.sqrt(determinant(m))

#### Argument Parsing and Sanity Checks ####

# NOTE: Inputting the matrices is not implemented yet. For now just edit the
# values for g and h to change them.

g = [1, 0, 0, 1]
h = [1, 0, 0, 1]

if determinant(g) != 1:
    print("Error: The matrix g is not in SL(2,Z).")
    sys.exit(1)

if determinant(h) != 1:
    print("Error: The matrix h is not in SL(2,Z).")
    sys.exit(1)

#### Algorithm Cases ####

def caseOne(g, h):
    print("Error: Case I is not implemented yet.")
    sys.exit(1)

def caseTwo(g, h):
    print("Error: Case II is not implemented yet.")
    sys.exit(1)

def caseThree(g, h):
    print("Error: Case III is not implemented yet.")
    sys.exit(1)

#### Algorithm Start ####

print("Inputted matrices:")
print()
print(f"g = {g}")
print(f"h = {h}")
print()

if T(g) < 0:
    g = negate(g)

if T(h) < 0:
    h = negate(h)

if T(g) > T(h):
    g, h = h, g

if T(g) > 2:
    caseOne(g, h)
elif T(g) == 2 and T(h) > 2:
    caseTwo(g, h)
elif T(g) == 2 and T(h) == 2:
    caseThree(g, h)
else:
    print("Result: The subgroup < g, h > is either not free or not discrete.")
