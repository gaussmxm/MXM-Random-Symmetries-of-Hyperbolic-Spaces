# Partial implementation of the algorithm in "An Algorithm for 2-Generator
# Fuchsian Groups" by J. Gilman and B. Maskit (doi:10.1307/mmj/1029004258).

# The algorithm takes as input two entries of SL(2,Z) and decides whether or
# not the subgroup of PSL(2,Z) that they generate is non-elementary, free, and
# discrete.

#### Imports ####

import math
import sys

#### Common Methods ####

def crossRatio(rg, ag, rh, ah):
    return ((rg - rh) * (ag - ah)) / ((rg - ah) * (ag - rh))

def determinant(m):
    return (m[0] * m[3]) - (m[1] * m[2])

def invert(m)
    return [m[3], -m[1], -m[2], m[0]]

def negate(m):
    return [-m[0], -m[1], -m[2], -m[3]]

def trace(m):
    return m[0] + m[3]

#### Argument Parsing and Sanity Checks ####

# NOTE: Inputting the matrices is not implemented yet. For now just edit the
# values for g and h to change them.

g = [2, 3, 1, 2]
h = [2, 3, 1, 2]

if determinant(g) != 1:
    print("Error: The matrix g is not in SL(2,Z).")
    sys.exit(1)

if determinant(h) != 1:
    print("Error: The matrix h is not in SL(2,Z).")
    sys.exit(1)

#### Algorithm Cases ####

def caseOne(g, h):
    if trace(g) > trace(h):
        g, h = h, g

    # NOTE: I have not proved that there is always exactly one attracting and
    # one repelling fixed point. This computation assumes that here.

    ag = ((g[0] - g[3]) + math.sqrt(((trace(g)) ** 2) - 4)) / (2 * g[2])
    rg = ((g[0] - g[3]) - math.sqrt(((trace(g)) ** 2) - 4)) / (2 * g[2])

    if (((g[2] * ag) + g[3]) ** 2) < 1:
        ag, rg = rg, ag

    ah = ((h[0] - h[3]) + math.sqrt(((trace(h)) ** 2) - 4)) / (2 * h[2])
    rh = ((h[0] - h[3]) - math.sqrt(((trace(h)) ** 2) - 4)) / (2 * h[2])

    if (((h[2] * ah) + h[3]) ** 2) < 1:
        ah, rh = rh, ah

    if ag == ah or rg == rh or ag == rh or rg == ah:
        print("Result: The subgroup < g, h > is either not discrete", end = '')
        print(" or elementary.")
        sys.exit(0)

    if crossRatio(rg, ag, rh, ah) > 1:
        h = invert(h)

    print("Error: Case I is not fully implemented yet.")
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

if trace(g) < 0:
    g = negate(g)

if trace(h) < 0:
    h = negate(h)

if trace(g) > trace(h):
    g, h = h, g

if trace(g) > 2:
    caseOne(g, h)
elif trace(g) == 2 and trace(h) > 2:
    caseTwo(g, h)
elif trace(g) == 2 and trace(h) == 2:
    caseThree(g, h)
else:
    print("Result: The subgroup < g, h > is either not free or not discrete.")
