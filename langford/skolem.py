"""Python implementations of various Skolem Sequence constructions.
Nabil Shalaby's PhD Thesis: Skolem Sequences, Generalizations and Applications
is a key source for most of these implementations.
"""

def skolem(n):
    """Generates a Skolem sequence as a list of tuples.
     See Theorem I.1 in Nabil Shalaby's PhD Thesis
    """

    necessary_conditions = \
        (n > 0) and (
            (n % 4 == 0) or
            (n % 4 == 1)
        )

    if not necessary_conditions:
        raise ValueError("Invalid value of n")

    if n % 4 == 0:
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
    else: # n % 4 == 1
        if n == 1:
            # (1,1)
            return [(1,2)]
        if n == 5:
            # (2,4,2,3,5,4,3,1,1,5)
            return [(8,9), (1,3), (4, 7), (2, 6), (5, 10)]

        seq = []
        s = (n - 1) // 4
        for r in range(1, 2*s + 1):
            seq.append((4 * s + r + 1, 8 * s - r + 3))
            
        for r in range(1, s + 1):
            seq.append((r, 4 * s - r + 1))
        
        for r in range(1, s - 2 + 1):
            seq.append((s + r + 2, 3 * s - r + 1))
        
        seq.append((s+1, s+2))
        seq.append((2*s+1, 6*s+2))
        seq.append((2*s+2, 4*s+1))
        return seq

