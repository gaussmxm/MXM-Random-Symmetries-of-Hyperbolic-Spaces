import argparse
import multiprocessing

def trace(m):
    return m[0] + m[3]

def invert(m):
    return (m[3], -m[1], -m[2], m[0])

def commutator(m1, m2):
    return m_mult(m_mult(invert(m1), invert(m2)), m_mult(m1, m2))

def negate(m):
    return (-m[0], -m[1], -m[2], -m[3])

def m_mult(m1, m2):
    return ((m1[0] * m2[0]) + (m1[1] * m2[2]),
            (m1[0] * m2[1]) + (m1[1] * m2[3]),
            (m1[2] * m2[0]) + (m1[3] * m2[2]),
            (m1[2] * m2[1]) + (m1[3] * m2[3]))

def is_free(X, Y):
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

        m = min(trace(m_mult(X, Y)), trace(m_mult(invert(X), Y)))

        if abs(m) < 2:
            return False

        if m >= 2:
            if trace(m_mult(X, Y)) == m:
                Y = m_mult(X, Y)
            else:
                Y = m_mult(invert(X), Y)
        else:
            return True

def compute_pairs(args):
	curr = args[0]
	matrices_tmp = args[1]

	if abs(trace(matrices_tmp[curr])) < 2:
		return 0
	else:
		num_free = 0

		for k in range(curr, len(matrices_tmp)):
			if is_free(matrices_tmp[curr], matrices_tmp[k]):
				num_free += 1
		
		return num_free

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = "Compute proportions of free groups.")
	parser.add_argument("radius", type = int, help = "radius of open ball to compute in")
	radius = parser.parse_args().radius

	if radius <= 0:
		parser.error("radius must be positive")

	a = (0, -1, 1, 0)
	b = (1, 1, 0, 1)

	generators = [a, invert(a), b, invert(b)]
	matrices = set([(1, 0, 0, 1)])

	for i in range(0, radius):
		tmp_matrices = set()

		for n in matrices:
			for m in generators:
				tmp = m_mult(n, m)

				if tmp not in matrices:
					tmp_matrices.add(tmp)
					
		matrices = matrices.union(tmp_matrices)
		
		num_free = 0
		
		matrices_tmp = list(matrices)
		matrices_tmp.sort(key = lambda m : abs(trace(m)))

		with multiprocessing.Pool(12) as p:
			for f in p.imap_unordered(compute_pairs, ((j, matrices_tmp) for j in range(0, len(matrices_tmp))), 100):
				num_free += f

		percentage = (2 * num_free) / (len(matrices_tmp) * (len(matrices_tmp) + 1))

		print("%2d : %.5f" % (i + 1, percentage))
