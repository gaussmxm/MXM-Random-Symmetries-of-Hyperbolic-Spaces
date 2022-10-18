import argparse
import itertools
import multiprocessing

def tr(m):
    return m[0] + m[3]

def inv(m):
    return (m[3], -m[1], -m[2], m[0])

def comm(m1, m2):
    return mult(mult(inv(m1), inv(m2)), mult(m1, m2))

def negate(m):
    return (-m[0], -m[1], -m[2], -m[3])

def mult(m1, m2):
    return ((m1[0] * m2[0]) + (m1[1] * m2[2]),
            (m1[0] * m2[1]) + (m1[1] * m2[3]),
            (m1[2] * m2[0]) + (m1[3] * m2[2]),
            (m1[2] * m2[1]) + (m1[3] * m2[3]))

def is_free(args):
    X = args[0]
    Y = args[1]

    if abs(tr(X)) < 2 or abs(tr(Y)) < 2:
        return 0

    if tr(comm(X, Y)) <= 2 and tr(comm(X, Y)) > -2:
        return 0

    if tr(comm(X, Y)) <= -2:
        return 1

    if tr(X) < 0:
        X = negate(X)

    if tr(Y) < 0:
        Y = negate(Y)

    while True:
        if tr(X) > tr(Y):
            X, Y = Y, X

        m = min(tr(mult(X, Y)), tr(mult(inv(X), Y)))

        if abs(m) < 2:
            return 0

        if m >= 2:
            if tr(mult(X, Y)) == m:
                Y = mult(X, Y)
            else:
                Y = mult(inv(X), Y)
        else:
            return 1

parser = argparse.ArgumentParser(description = "Compute proportions of free groups.")
parser.add_argument("radius", type = int, help = "radius of open ball to compute in")
radius = parser.parse_args().radius

if radius < 0:
    parser.error("radius must be nonnegative")

a = (1, 0, 1, 1)
b = (1, 1, 0, 1)

generators = [a, inv(a), b, inv(b)]
matrices = set([(1, 0, 0, 1)])

if __name__ == "__main__":
    for i in range(0, radius):
        matrices.update(mult(n, m) for (n, m) in itertools.product(matrices, generators))

        with multiprocessing.Pool(6) as p:
            total = sum(p.imap(is_free, itertools.combinations(matrices, 2), 10000))

        print("[%2d] %.5f" % (i + 1, (2 * total) / (len(matrices) ** 2)))
