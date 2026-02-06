

def skolem(n):
    """Generates a skolem sequence as a list of tuples assuming n % 4 == 0"""
    seq = []
    s = n // 4
    for r in range(1, 2 * s + 1):
        seq.append((4 * s + r - 1, 8 * s - r + 1))
    
    for r in range(1, s - 2 + 1):
        seq.append((r, 4*s - r - 1))
    
    for r in range(1, s - 2 + 1):
        seq.append((s + r + 1, 3 * s - r))

    seq.append((s - 1, 3 * s))
    seq.append((s, s + 1))
    seq.append((2 * s, 4 * s - 1))
    seq.append((2 * s + 1, 6 * s))
    return seq


n = 4 * 3
seq = skolem(n)

for index, (a,b) in enumerate(seq):
    r = index + 1

    print(b + n, a + n, b - a)