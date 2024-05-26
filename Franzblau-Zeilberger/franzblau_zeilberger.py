def Chop(lam):
    i = 0
    while i < len(lam) and lam[i] > 0:
        i += 1
    return lam[:i]

def BadElem(T):
    if not T or not any(T):
        return "ERROR: There is no Tableau!"

    trans = Transpose(T)
    bad = [0, 0, 0]

    for j in range(len(T[0])):
        for i in range(len(trans[j]) - 1):
            if T[i + 1][j] < T[i][j] and (T[i + 1][j] < bad[0] or bad[0] == 0):
                bad = [T[i + 1][j], i + 2, j + 1]

    return bad

def SatisfyDC(T, d):
    satisfy = []
    for j in range(1, len(d)):
        temp1 = d[j]
        yj = int(temp1[1:])
        temp2 = d[j - 1]
        v = int(temp2[1:])
        check = False
        print(f"Checking T[{j}]: {T[j-1]} with yj={yj} and T[{j-1}]: {T[j-2]}")

        for t in range(v + 1, yj + 1):
            if yj <= len(T[j - 1]) and t <= len(T[j]) and t <= len(T[j - 1]):
                print(f"Comparing T[{j}][{t-1}]={T[j][t-1]} with T[{j-1}][{t}]={T[j-1][t]}")
                if T[j][t - 1] < T[j - 1][t]:
                    check = True
            else:
                print(f"Skipping invalid comparison with t={t}, yj={yj}")

        if temp1[0] == 'C' and (temp2[0] == 'R' or (v < yj and check)):
            if yj <= len(T[j]):
                satisfy.append([T[j][yj - 1], j, yj])
            else:
                print(f"Skipping invalid append with yj={yj} and T[{j}] length={len(T[j])}")

    return satisfy

def BuildS(d, S):
    if len(d) < len(S):
        return "d is too small to adjoin to S"
    Snew = [[] for _ in range(len(d))]
    for i in range(len(d)):
        if i < len(S):
            Snew[i] = [d[i][0]] + S[i]
        else:
            Snew[i] = d[i]
    return Snew

def Transpose(YT):
    if not YT:
        return []
    max_len = max(len(row) for row in YT)
    transposed = [[YT[i][j] if j < len(YT[i]) else None for i in range(len(YT))] for j in range(max_len)]
    return [[elem for elem in row if elem is not None] for row in transposed]

def RSORT(YT):
    T = []
    S = []
    trans = Transpose(YT)
    for K in range(len(YT[0]), 0, -1):
        a = trans[K - 1]
        print(f"Processing column {K}: {a}")
        temp = IC(a, T, S)
        T = temp[0]
        S = temp[1]
        print(f"Intermediate T: {T}")
        print(f"Intermediate S: {S}")
    return [T, S]

def FINDR(T, S):
    Tnew = T
    Snew = S
    trans = [[] for _ in range(len(T[0]))]
    for K in range(1, len(T[0]) + 1):
        temp = DC(Tnew, Snew)
        trans[K - 1] = temp[0]
        Tnew = temp[1]
        Snew = temp[2]
        print(f"Step {K}: trans={trans}, Tnew={Tnew}, Snew={Snew}")
    return Transpose(trans)

def INSERT1(aj, j, T):
    if j == len(T) + 1:
        newj = [aj]
        i = 1
    elif j == 0 or j > len(T) + 1:
        return "ERROR: row index not expected in INSERT1"
    else:
        row = T[j - 1]
        i = 0
        while i < len(row) and aj > row[i]:
            i += 1
        newj = row[:i] + [aj] + row[i:]
    Tnew = T[:j - 1] + [newj] + T[j:]
    return Tnew, i + 1

def REMOVE1(i, j, T):
    if i == 0 or i > len(T):
        return "ERROR: row index not expected in REMOVE1"
    if j == 0 or j > len(T[i - 1]):
        return "ERROR: column index not expected in REMOVE1"
    row = T[i - 1]
    newi = row[:j - 1] + row[j:]
    Tnew = T[:i - 1] + [newi] + T[i:]
    return Tnew

def SIMPLIFY1(T):
    return [row for row in T if row]

def EXCHANGE2(i1, j1, i2, j2, T):
    if i1 > len(T) or i1 == 0 or i2 > len(T) or i2 == 0:
        return "ERROR: row index does not exist in T"
    Tnew = REMOVE1(i1, j1, T)
    Tnew = REMOVE1(i2, j2, Tnew)
    temp = INSERT1(T[i2 - 1][j2 - 1], i1, Tnew)
    Tnew = temp[0]
    j2new = temp[1]
    temp = INSERT1(T[i1 - 1][j1 - 1], i2, Tnew)
    Tnew = temp[0]
    j1new = temp[1]
    return Tnew, j1new, j2new

def IC(a, T, S):
    Tnew = T
    d = [None] * len(a)
    for j in range(len(a)):
        temp = INSERT1(a[j], j + 1, Tnew)
        Tnew = temp[0]
        d[j] = f'C{temp[1]}'
    bad = BadElem(Tnew)
    while bad != [0, 0, 0]:
        k = bad[1]
        x = bad[2]
        y = int(d[k - 1][1:])
        temp = EXCHANGE2(k, x, k - 1, y, Tnew)
        Tnew = temp[0]
        yprime = temp[2]
        up = d[k]
        if up[0] == 'R':
            d[k - 1] = f'R{int(up[1:]) + 1}'
        elif up[0] == 'C' and int(up[1:]) == x:
            d[k - 1] = 'R2'
        else:
            d[k - 1] = d[k]
        d[k] = f'C{yprime}'
        bad = BadElem(Tnew)
    Snew = BuildS([[d[i]] for i in range(len(a))], S)
    return Tnew, Snew
def DC(T, S):
    d = [S[j][0] for j in range(len(T))]
    satisfy = SatisfyDC(T, d)
    max_val = 0
    Tnew = T
    Snew = S
    while satisfy:
        for item in satisfy:
            ajyj, j, yj = item
            r = 0
            for t in range(2, yj + 1):
                if t <= len(T[j - 1]) and t <= len(T[j - 2]):
                    if T[j - 1][t - 1] < T[j - 2][t - 1]:
                        r = t
            sj = 1 if r == 0 or d[j - 1] == 'C1' else r
            if max_val < T[j - 2][sj - 1]:
                max_val = T[j - 2][sj - 1]
                k, y, s = j, yj, sj
        temp = EXCHANGE2(k - 1, s, k, y, Tnew)
        Tnew = temp[0]
        yprime = temp[2]
        up = d[k - 1]
        if d[k - 1] == 'R2':
            d[k] = f'C{s}'
        elif up[0] == 'C':
            d[k] = d[k - 1]
        else:
            d[k] = f'R{int(up[1:]) - 1}'
        d[k - 1] = f'C{yprime}'
        max_val = 0
        satisfy = SatisfyDC(Tnew, d)
    a = []
    for j in range(1, len(Tnew) + 1):
        if int(d[j - 1][1:]) - 1 < len(Tnew[j - 1]):
            a.append(Tnew[j - 1][int(d[j - 1][1:]) - 1])
        else:
            print(f"Skipping invalid access: d[{j-1}]={d[j-1]}, Tnew[{j-1}]={Tnew[j-1]}")
    for j in range(1, len(Tnew) + 1):
        if int(d[j - 1][1:]) - 1 < len(Tnew[j - 1]):
            Tnew = REMOVE1(j, int(d[j - 1][1:]), Tnew)
            Snew = REMOVE1(j, 1, Snew)
    Tnew = SIMPLIFY1(Tnew)
    Snew = SIMPLIFY1(Snew)
    return a, Tnew, Snew
