# Implementation of the algorithm in "An Algorithm for 2-Generator Fuchsian
# Groups" by J. Gilman and B. Maskit (doi:10.1307/mmj/1029004258).
#
# The program takes as input two matrices in GL(2,Z) that have positive
# determinants and determines whether the subgroup of PSL(2,R) that they
# generate is non-elementary, free, and discrete.

# NOTE: Once we hit an elliptic element, we are done; the subgroup is either
# not free or not discrete (see the middle of page 14 in the paper).

# Matrices are represented by lists with 4 elements. For example, the matrix
#
# [ a b ]
# [ c d ]
#
# is encoded as the list [a, b, c, d].

#### Imports ####

import math
import sys

#### Common Methods ####

# Computes the trace of the matrix m.

def trace(m):
    return m[0] + m[3]

# Computes the determinant of the matrix m.

def determinant(m):
    return (m[0] * m[3]) - (m[1] * m[2])

# Computes the product m1 * m2 of the matrices m1 and m2.

def matrixMultiply(m1, m2):
    return [(m1[0] * m2[0]) + (m1[1] * m2[2]),
            (m1[0] * m2[1]) + (m1[1] * m2[3]),
            (m1[2] * m2[0]) + (m1[3] * m2[2]),
            (m1[2] * m2[1]) + (m1[3] * m2[3])]

# Compute the quantity used throughout the algorithm for the matrix m. The
# quantity is given by T(m) = tr(m) / sqrt(det(m)). Note that this quantity is
# always well-defined, since the matrices we work with always have positive
# determinants.

def T(m):
    return trace(m) / math.sqrt(determinant(m))

#### Argument Parsing and Sanity Checks ####

# NOTE: This method of reading in the matrices is quite ugly. Don't @ me.
#
# For a pair of matrices g = [a, b, c, d] and h = [w, x, y, z], invoke the
# program as
#
# python3 program.py a b c d w x y z
#
# to run the algorithm on g and h.

if len(sys.argv) != 9:
    print("Error: Expected 8 arguments (2 matrices, 4 entries each).")
    sys.exit(1)

for i in range(1, 9):
    try:
        sys.argv[i] = int(sys.argv[i])
    except:
        print("Error: Could not parse an argument into an integer.")
        sys.exit(1)

g = sys.argv[1:5]
h = sys.argv[5:]

# NOTE: End of ugliness.

if determinant(g) <= 0:
    print("Error: Matrix g does not have positive determinant.")
    sys.exit(1)

if determinant(h) <= 0:
    print("Error: Matrix h does not have positive determinant.")
    sys.exit(1)

#### 0. First Computations ####

#### 1. Hyperbolic-Hyperbolic ####

#### 2. Hyperbolic-Parabolic ####

#### 3. Parabolic-Parabolic ####

#### 4. Elliptic-Hyperbolic ####

#### 5. Elliptic-Parabolic ####

#### 6. Elliptic-Elliptic ####
