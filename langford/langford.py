from .skolem import skolem

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
    
    if (d == 1):
        return skolem(n)

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