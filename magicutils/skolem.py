

def skolem(n):
    """Generates a skolem sequence as a list of tuples assuming n % 4 == 0"""
    if n == 4:
        # (1,1,3,4,2,3,2,4)
        return [(1, 2), (5, 7), (3, 6), (4, 8)]
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
