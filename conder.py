#!/usr/bin/env python3

# Freeness algorithm from "Discrete and free subgroups of SL_2" by Matthew Conder, p. 15.

import itertools
import sys

def trace(m):
    return m[0] + m[3]

def invert(m):
    return (m[3], -m[1], -m[2], m[0])

def commutator(m1, m2):
    return matrixMult(matrixMult(invert(m1), invert(m2)), matrixMult(m1, m2))

def determinant(m):
    return (m[0] * m[3]) - (m[1] * m[2])

def negate(m):
    return (-m[0], -m[1], -m[2], -m[3])

def matrixMult(m1, m2):
    return ((m1[0] * m2[0]) + (m1[1] * m2[2]),
            (m1[0] * m2[1]) + (m1[1] * m2[3]),
            (m1[2] * m2[0]) + (m1[3] * m2[2]),
            (m1[2] * m2[1]) + (m1[3] * m2[3]))

def isFree(X, Y):
    if abs(trace(X)) < 2 or abs(trace(Y)) < 2:
        return False

    if trace(commutator(X, Y)) <= 2 and trace(commutator(X, Y)) > -2:
        return False

    if trace(commutator(X, Y)) <= -2:
        return True

    if trace(X) < 0:
        X = negate(X)

    if trace(Y) < 0:
        Y = negate(Y)

    while True:
        if trace(X) > trace(Y):
            X, Y = Y, X

        m = min(trace(matrixMult(X, Y)), trace(matrixMult(invert(X), Y)))

        if abs(m) < 2:
            return False

        if m >= 2:
            if trace(matrixMult(X, Y)) == m:
                Y = matrixMult(X, Y)
            else:
                Y = matrixMult(invert(X), Y)
        else:
            return True

a = (0, -1, 1, 0)
b = (1, 1, 0, 1)

generators = [a, invert(a), b, invert(b)]

if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " [DISTANCE]")
    sys.exit(1)

radius = 0

try:
    radius = int(sys.argv[1])
except:
    print("Error: Could not parse distance.")
    sys.exit(1)

if radius < 0:
    print("Error: Distance not >= 0.")
    sys.exit(1)

matrices = set([(1, 0, 0, 1)])

for i in range(0, radius):
    tmp_matrices = set()

    for n in matrices:
        for m in generators:
            tmp = matrixMult(m, n)

            if tmp not in matrices and tmp not in tmp_matrices:
                tmp_matrices.add(tmp)
                
    matrices = matrices.union(tmp_matrices)
    
numFree = 0
numTotal = 0

# This is the big slowdown - the number of pairs we need to check is O(n^2), where n
# is the number of matrices we have generated. Generating the matrices themselves is
# much faster in comparison.

for n in itertools.combinations_with_replacement(matrices, 2):
    numTotal += 1

    if isFree(n[0], n[1]):
        numFree += 1
    
percentage = numFree / numTotal

print("Proportion of pairs that generate a free group: %.3f" % percentage)
