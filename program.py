#!/usr/bin/env python3

# Implementation of the algorithm presented in "An Algorithm for 2-Generator
# Fuchsian Groups" by J. Gilman and B. Maskit (doi:10.1307/mmj/1029004258).

# The program takes as input two entries of SL(2,Z) and decides if the subgroup
# of PSL(2,R) that they generate is non-elementary, free, and discrete.

import math
import sys

# NOTE: This method will cause a problem if you don't check beforehand that
# the result is infinite.

def apply(m, z):
    return ((m[0] * z) + m[1]) / ((m[2] * z) + m[3])

def caseOne(g, h):
    if trace(g) > trace(h):
        g, h = h, g

    ag = ((g[0] - g[3]) + math.sqrt((trace(g) ** 2) - 4)) / (2 * g[2])
    rg = ((g[0] - g[3]) - math.sqrt((trace(g) ** 2) - 4)) / (2 * g[2])

    ah = ((h[0] - h[3]) + math.sqrt((trace(h) ** 2) - 4)) / (2 * h[2])
    rh = ((h[0] - h[3]) - math.sqrt((trace(h) ** 2) - 4)) / (2 * h[2])

    # NOTE: Float comparison?

    if ag == ah or rg == rh or ag == rh or rg == ah:
        print("Result: The subgroup < g, h > is either not discrete", end = "")
        print(" or elementary.")
        sys.exit(0)

    if crossRatio(rg, ag, rh, ah) > 1:
        h = invert(h)

    if crossRatio(rg, ag, rh, ah) > 0:
        if jorgensenNumber(g, h) < 1:
            print("Result: The subsgroup < g, h > is not discrete.")
            sys.exit(0)

        if trace(matrixMult(g, h)) < -2:
            print("Result: The subgroup < g, h > is non-elementary,", end = "")
            print(" free, and discrete.")
            sys.exit(0)

        if abs(trace(matrixMult(g, h))) == 2:
            caseTwo(g, matrixMult(g, h))

        if abs(trace(matrixMult(g, h))) < 2:
            print("Result: The subgroup < g, h > is either not ", end = "")
            print("free or not discrete.")
            sys.exit(0)
        
        # NOTE: Does it matter if we use gh, g or -gh, g?

        caseOne(matrixMult(g, h), g)
    else:
        if trace(commutator(g, h)) <= -2:
            print("Result: The subgroup < g, h > is non-elementary,", end = "")
            print(" free, and discrete.")
            sys.exit(0)
        else:
            print("Result: The subgroup < g, h > is either not ", end = "")
            print("free or not discrete.")
            sys.exit(0)

def caseTwo(g, h):
    print("Error: Case II is not implemented yet.")
    sys.exit(1)

    if trace(g) > trace(h):
        g, h = h, g

    ah = ((h[0] - h[3]) + math.sqrt((trace(h) ** 2) - 4)) / (2 * h[2])
    rh = ((h[0] - h[3]) - math.sqrt((trace(h) ** 2) - 4)) / (2 * h[2])

    isInf = True
    fg = 0

    if g[2] != 0:
        isInf = False
        fg = (g[0] - g[3]) / (2 * g[2])

    if not isInf and (fg == ah or fg == rh):
        print("Result: The subgroup < g, h > is not discrete.")
        sys.exit(0)

    # NOTE: Steps II-2, II-3 are missing

    if abs(h[1] * g[1]) < 1:  
        print("Result: The subgroup < g, h > is not discrete.")
        sys.exit(0)

    if trace(matrixMult(g, h)) < -2:
        print("Result: The subgroup < g, h > is non-elementary, ", end = "")
        print("free, and discrete.")
        sys.exit(0)

    if abs(trace(matrixMult(g, h))) < 2: 
        print("Result: The subgroup < g, h > is either not free or ", end = "")
        print("not discrete.")
        sys.exit(0)

    if trace(matrixMult(g, h)) == 2:
        caseThree(g, matrixMult(g, h))

    caseTwo(g, matrixMult(g, h))

def caseThree(g, h):

    if trace(g) < 0:
        g = negate(g)

    if trace(h) < 0:
        h = negate(h)

    isInfg = True
    fg = 0

    if g[2] != 0:
        isInfg = False
        fg = (g[0] - g[3]) / (2 * g[2])

    isInfh = True
    fh = 0

    if h[2] != 0:
        isInfh = False
        fh = (h[0] - h[3]) / (2 * h[2])

    if (isInfg and isInfh) or (not isInfg and not isInfh and fg == fh):
        print("Result: The subgroup < g, h > is elementary.")
        sys.exit(0)

    C = 0

    if isInfg:
        if h[0] == -h[3]:
            C = 1
        else:
            C = (fh - apply(g, fh)) / (fh - (h[0] / h[2]))
    elif isInfh:
        if g[0] == -g[3]:
            C = 1
        else:
            C = (fg - apply(h, fg)) / (fg - (g[0] / g[2]))
    else:

        # NOTE: Not finished here yet.

        print("Error: Case III is not fully implemented yet (two ", end = "")
        print("non-infinite fixed points.")
        sys.exit(1)

    if C > 0:
        h = invert(h)

    if abs(trace(matrixMult(g, h))) < 2:
        print("Result: The subgroup < g, h > is either not free or ", end = "")
        print("not discrete.")
        sys.exit(0)

    print("Result: The subgroup < g, h > is non-elementary, free, ", end = "")
    print("and discrete.")
    sys.exit(0)

def commutator(g, h):
    return matrixMult(matrixMult(invert(g), invert(h)), matrixMult(g, h))

def crossRatio(rg, ag, rh, ah):
    return ((rg - rh) * (ag - ah)) / ((rg - ah) * (ag - rh))

def determinant(m):
    return (m[0] * m[3]) - (m[1] * m[2])

def invert(m):
    return [m[3], -m[1], -m[2], m[0]]

def jorgensenNumber(g, h):
    return abs(trace(commutator(g, h)) - 2) + abs((trace(g) ** 2) - 4)

def matrixMult(m1, m2):
    return [(m1[0] * m2[0]) + (m1[1] * m2[2]),
            (m1[0] * m2[1]) + (m1[1] * m2[3]),
            (m1[2] * m2[0]) + (m1[3] * m2[2]),
            (m1[2] * m2[1]) + (m1[3] * m2[3])]

def negate(m):
    return [-m[0], -m[1], -m[2], -m[3]]

def trace(m):
    return m[0] + m[3]

# NOTE: Inputting the matrices from the commandline is not implemented yet, so
# for now just edit the definitions of g and h here to change them.

g = [1, 0, 0, 1]
h = [1, 0, 0, 1]

print()
print(f"g = {g}")
print(f"h = {h}")
print()

if determinant(g) != 1:
    print("Error: The matrix g is not in SL(2,Z).")
    sys.exit(1)

if determinant(h) != 1:
    print("Error: The matrix h is not in SL(2,Z).")
    sys.exit(1)

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
    sys.exit(0)
