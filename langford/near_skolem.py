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