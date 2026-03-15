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


def langford(n, d):
    """Construct a Langford sequence of order n with defect d.
    See J. E. Simpson, Langford sequences: Perfect and hooked, Discrete Math. 44 (1983)97-104. ⟨613⟩
    for defects other than 2. Specifically, they show constructions for even orders but cite other works
    for the other possibilities.
    We have only implemented his constructions so far...
    """

    necessary_conditions = \
    (n > 0) and (d > 0) and (n >= (2 * d - 1)) and (
            (((n % 4 == 0) or (n % 4 == 1)) and (d % 2 == 1))
        or  (((n % 4 == 0) or (n % 4 == 3)) and (d % 2 == 0))
    )

    if not necessary_conditions:
        raise ValueError(f"No Langford sequence exists when n={n} and d={d}.")
    
    if (n % 4) != 0:
        raise NotImplementedError("Only the case of when n = 0 (mod 4) has been implemented...")

    # Simpson's case 1: d = 0 (mod 4)
    if (n % 4 == 0) and (d % 4 == 0):
        t = n // 4
        s = d // 4

        seq = []
        # Row 1 (omit when t = 2s)
        if t != 2 * s:
            seq += [(2*t-3*s+1-j, 2*t+s+2+j) for j in range((t - 2 * s - 1) + 1)]
        # Row 2
        seq += [(t-2*s+1-j, 3*t+s+1+j) for j in range((t - 2 * s) + 1)]
        # Row 3 (omit when t = 2s)
        if t != 2 * s:
            seq += [(6*t-s+1-j, 6*t+3*s+1+j) for j in range((t - 2*s - 1) + 1)]
        # Row 4
        seq += [(5*t-s+1-j, 7*t+2*s+j) for j in range((t - 2 * s) + 1)]
        # Row 5
        seq += [(3*t-s+2, 5*t-s+2)]
        # Row 6
        seq += [(2*t-j, 4*t+1+j) for j in range((s-1) + 1)]
        # Row 7 (Omit if s = 1)
        if s != 1:
            seq += [(4*t-s+2+j, 6*t+s+2+2*j) for j in range((s - 2) + 1)]
        # Row 8 (Omit if s = 1)
        if s != 1:
            seq += [(3*t+1-j, 5*t+3+j) for j in range((s - 2) + 1)]
        # Row 9 (Omit if s = 1)
        if s != 1:
            seq += [(3*t+s-j, 7*t+s+1+j) for j in range((s-2) + 1)]
        # Row 10
        seq += [(t-s+1-j, 5*t-s+3+j) for j in range((s-1) + 1)]
        # Row 11
        seq += [(2*t-3*s+2+j, 6*t-s+3+2*j) for j in range((2*s - 2) + 1)]
        # Row 12
        seq += [(2*t+1+j, 6*t-s+2+2*j) for j in range((s-1) + 1)]
        # Row 13
        seq += [(2*t+s+1, 6*t+3*s)]

        return seq

    # Simpson's case 2: d = 2 (mod 4)
    if (n % 4 == 0) and (d % 4 == 2):
        t = n // 4
        s = (d - 2) // 4

        if (s == 0) and (d == 2):
            raise NotImplementedError("See Davies")
        seq = []
        # Row 1 (omit if t = 2s + 1)
        if t != 2*s+1:
            # I'm not 100% sure that this is correct. The scanned version is hard to read here.
            seq += [(2*t-3*s-1-j, 2*t+s+2+j) for j in range((t-2*s-2)+1)]
        # Row 2
        seq += [(t-2*s-j,3*t+s+1+j) for j in range((t-2*s-1)+1)]
        # Row 3 (omit if t = 2s + 1)
        if t != 2*s+1:
            seq += [(6*t-s-j, 6*t+3*s+2+j) for j in range((t-2*s-2)+1)]
        # Row 4 (omit if t = 2s + 1)
        if t != 2*s+1:
            seq += [(5*t-s-1-j,7*t+2*s+1+j) for j in range((t-2*s-2)+1)]
        # Row 5
        seq += [(5*t-s, 7*t+s+1)]
        # Row 6
        seq += [(2*t-j, 4*t+1+j) for j in range((s-1)+1)]
        # Row 7 (omit if s = 1)
        if s != 1:
            seq += [(4*t-s+1+j, 6*t+s+3+2*j) for j in range((s-2)+1)]
        # Row 8
        seq += [(3*t+1-j, 5*t+1+j) for j in range((s)+1)]
        # Row 9 (omit if s = 1)
        if s != 1:
            seq += [(3*t+s-j, 7*t+s+2+j) for j in range((s-2)+1)]
        # Row 10
        seq += [(t-s-j,5*t-s+1+j) for j in range((s-1)+1)]
        # Row 11
        seq += [(2*t-3*s+j, 6*t-s+2+2*j) for j in range((2*s-1)+1)]
        # Row 12
        seq += [(2*t+1+j, 6*t-s+1+2*j) for j in range((s-1)+1)]
        # Row 13
        seq += [(2*t+s+1,6*t+3*s+1)]
        # Row 14
        seq += [(2*t-s,6*t+s+1)]
        # Row 15
        seq += [(4*t, 8*t)]

        return seq
    # Simpson case 3: d = 3 (mod 4)
    if (n % 4 == 0) and (d % 4 == 3):
        t = n // 4
        s = (d + 1) // 4
        seq = []
        # Row 1 (omit if t = 2s)
        if t != 2*s:
            seq += [(2*t-3*s+1-j,2*t+s+1+j) for j in range((t-2*s-1)+1)]
        # Row 2
        seq += [(t-2*s+2-j,3*t+s+j) for j in range((t-2*s+1)+1)]
        # Row 3
        seq += [(6*t-s-j, 6*t+3*s-1+j) for j in range((t-2*s)+1)]
        # Row 4
        seq += [(5*t-s+1-j, 7*t+2*s+j) for j in range((t-2*s)+1)]
        # Row 5 (omit when s = 1)
        if s != 1:
            seq += [(3*t-s+1, 5*t-s+2)]
        # Row 6
        seq += [(2*t+1-j, 4*t+1+j) for j in range((s-1)+1)]
        # Row 7 (omit when s = 1)
        if s != 1:
            seq += [(4*t-s+2+j, 6*t+s+1+2*j) for j in range((s-2)+1)]
        # Row 8 (omit when s = 1 or s = 2)
        if (s != 1) and (s != 2):
            seq += [(3*t-1-j, 5*t+2+j) for j in range((s-3)+1)]
        # Row 9
        seq += [(3*t+s-1-j, 7*t+s+j) for j in range((s-1)+1)]
        # Row 10 (omit when s = 1)
        if s != 1:
            seq += [(t-s+1-j, 5*t-s+3+j) for j in range((s-2)+1)]
        # Row 11
        seq += [(2*t-3*s+2+j, 6*t-s+2+2*j) for j in range((2*s-2)+1)]
        # Row 12 (omit when s = 1)
        if s != 1:
            seq += [(2*t+2+j, 6*t-s+3+2*j) for j in range((s-2)+1)]
        # Row 13
        seq += [(2*t-s+1, 6*t-s+1)]

        return seq

    # Simpson's case 4: d = 1 (mod 4)
    if (n % 4 == 0) and (d % 4 == 1):
        t = n // 4
        s = (d - 1) // 4
        seq = []
        # Row 1 (omit if t = 2s + 1)
        if t != 2*s + 1:
            seq += [(2*t-3*s-1-j, 2*t+s+1+j) for j in range((t-2*s-2)+1)]
        # Row 2
        seq += [(t-2*s-j, 3*t+s+1+j) for j in range((t-2*s-1)+1)]
        # Row 3
        seq += [(6*t-s-1-j, 6*t+3*s+j) for j in range((t-2*s-1)+1)]
        # Row 4
        seq += [(5*t-s-j, 7*t+2*s+j) for j in range((t-2*s-1)+1)]
        # Row 5
        seq += [(t-s, 3*t+s)]
        # Row 6
        seq += [(2*t+1-j, 4*t+1+j) for j in range((s-1)+1)]
        # Row 7 (omit if s = 1)
        if s != 1:
            seq += [(4*t-s+1+j, 6*t+s+2+2*j) for j in range((s-2)+1)]
        # Row 8
        seq += [(3*t-1-j, 5*t+j) for j in range((s-1)+1)]
        # Row 9
        seq += [(3*t+s-1-j, 7*t+s+j) for j in range((s-1)+1)]
        # Row 10 (omit if s = 1)
        if s != 1:
            seq += [(t-s-1-j, 5*t-s+1+j) for j in range((s-2)+1)]
        # Row 11
        seq += [(2*t-3*s+j, 6*t-s+1+2*j) for j in range((2*s-1)+1)]
        # Row 12 (omit if s = 1)
        if s != 1:
            seq += [(2*t+2+j,6*t-s+2+2*j) for j in range((s-2)+1)]
        # Row 13
        seq += [(2*t-s+1, 6*t-s)]
        # Row 14
        seq += [(2*t-s, 6*t+s)]
        # Row 15
        seq += [(4*t, 8*t)]

        return seq


def near_skolem(n, m):
    """Create an order n near Skolem sequence with defect m"""

    necessary_conditions = \
        (n > 0) and (m > 0) and (m <= n) and (
               ((n % 4 == 0) and (m % 2 == 1))
            or ((n % 4 == 1) and (m % 2 == 1))
            or ((n % 4 == 2) and (m % 2 == 0))
            or ((n % 4 == 3) and (m % 2 == 0))
        )

    if not necessary_conditions:
        raise ValueError("Invalid values of n and m.")
    
    if (m == 1):
        # This is a perfect langford sequence with d = 1.
        # If m = 1, then m is odd. So, n = 0,1 (mod 4). Perfect Langford sequences exist whenever
        # m is odd and n = 0,1 (mod 4)
        # However, if m = 1, then the necessary conditions for a perfect Langford sequence
        # with d = 2 requires that 2d - 1 <= n. So, if n < 3, then what?
        # TODO: brute force solve the cases of n = 1, 2
        if n < 3:
            raise NotImplementedError("Do perfect Langford sequences even exist when n = 0,1 and m = 1?")
        return langford(n)
    

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
    
    raise NotImplementedError("There are 7 more cases to implement....")
    # TODO: implement rest of cases

