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
            (n % 4 == 0) or \
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


def perfect_langford(n, d):
    """Construct a perfect langford sequence of order n and defect d."""

    # necessary conditions as specified in the combinatorial handbook
    necessary_conditions = \
    (n >= (2 * d - 1)) and (
            (((n % 4 == 0) or (n % 4 == 1)) and (d % 2 == 1))
        or  (((n % 4 == 3) or (n % 4 == 4)) and (d % 2 == 0))
    )

    if not necessary_conditions:
        raise ValueError("Invalid values of n and d")
    
    raise NotImplementedError("Implement the constructive proof as specified in J. E. Simpson, Langford sequences: Perfect and hooked, Discrete Math. 44 (1983)97–104. ⟨613⟩")



def near_skolem(n, m):
    """Create a near order n skolem sequence with defect m"""

    necessary_conditions = \
       ((n % 4 == 0) and (m % 2 == 1))\
    or ((n % 4 == 1) and (m % 2 == 1))\
    or ((n % 4 == 2) and (m % 2 == 0))\
    or ((n % 4 == 3) and (m % 2 == 0))

    if not necessary_conditions:
        raise ValueError("Invalid values of n and m.")
    
    if (m == 1) and (n % 4 == 1):
        # This is a perfect langford sequence with d = 2
        # A perfect langford sequence exists
        # (according to combinatorial handbook) iff
        # n % 4 == 0, 3 and d is even
        # but Shalaby's proof assumes that a perfect Langford sequence exists in this case?
        raise ValueError("Invalid value of m and n")

    if (m == 1) and (n % 4 == 0):
        # construct a perfect Langford sequence of order n with defect 2
        return perfect_langford(n, 2)
    

    if n % 8 == 0:
        s = n // 8

        # m should be odd according to the necessary conditions
        t = (m - 1) // 2

        seq = []
        for r in range(0, 4 * s - t - 2 + 1):
            seq.append((8 * s + r - 1, 16 * s - r - 2))
        seq.append((12 * s - t - 2, 12*s - t - 1))
        for r in range(0, t - 2 + 1):
            seq.append((12 * s - t + r, 12 * s + t - r - 1))
        for r in range(0, 1 + 1):
            seq.append((4*s + r, 12 * s - r))
        for r in range(1, s - 1 + 1):
            seq.append((2 * r - 1, 8 * s - 2 * r - 3))
        for r in range(1, 2*s - 1 + 1):
            seq.append((2 * r, 8 * s - 2 * r))
        seq.append((2 * s - 1, 2 * s + 1))
        if n != 8:
            seq.append((4 * s - 1, 8 * s - 3))
        for r in range(s - 2):
            seq.append((2 * s + 2 * r + 1, 6 * s - 2 * r - 1))

        return seq


