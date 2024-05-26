import itertools
import random
import numpy as np

#-------------------------- Procedures for testing --------------------

def Perm2YT(pi, lambda_):
    if not pi:
        return []
    else:
        return [[*pi[:lambda_[0]]], *Perm2YT(pi[lambda_[0]:], lambda_[1:])]

def Perm2YT(pi, lambda_):
    if not pi:
        return []
    else:
        return [[*pi[:lambda_[0]]], *Perm2YT(pi[lambda_[0]:], lambda_[1:])]

def YT(lambda_):
    n = sum(lambda_)
    perms = itertools.permutations(range(1, n + 1))
    yt = set()
    for pi in perms:
        yt.add(tuple(map(tuple, Perm2YT(list(pi), lambda_))))
    return yt

def RandPerm(n):
    return random.sample(range(1, n + 1), n)

def RandNPS(lambda_):
    n = sum(lambda_)
    pi = RandPerm(n)
    T1 = Perm2YT(pi, lambda_)
    T2 = SPN(NPS(T1))
    if T1 != T2:
        raise ValueError(f"Bijection failed for tableau {T1}")

#-------------------------- Helper procedures --------------------

def LowerOrderTableau(T, c):
    M = np.zeros((len(T) + 1, len(T[0]) + 1), dtype=int)
    x, y = c
    for i in range(len(T)):
        for j in range(len(T[i])):
            if (j > y) or (j == y and i >= x):
                M[i, j] = T[i][j]
    return M

def isStandard(M):
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if M[i, j] != 0:
                if i > 0 and M[i - 1, j] > M[i, j]:
                    return False
                if j > 0 and M[i, j - 1] > M[i, j]:
                    return False
    return True

def ModifiedForwardSlide(T, c):
    c1 = c
    M = LowerOrderTableau(T, c1)
    T1 = T
    while not isStandard(M):
        i, j = c1
        if M[i + 1, j] == 0:
            cprime = [i, j + 1]
        elif M[i, j + 1] == 0:
            cprime = [i + 1, j]
        elif M[i + 1, j] > M[i, j + 1]:
            cprime = [i, j + 1]
        else:
            cprime = [i + 1, j]
        cvalue = M[i, j]
        M[i, j] = M[cprime[0], cprime[1]]
        M[cprime[0], cprime[1]] = cvalue
        cvalue = T1[i][j]
        T1[i][j] = T1[cprime[0]][cprime[1]]
        T1[cprime[0]][cprime[1]] = cvalue
        c1 = cprime
    return T1, c1

def CellOrder(T):
    if not T:
        return []
    i = 0 
    while i < len(T) - 1 and len(T[i + 1]) == len(T[0]):
        i += 1
    if len(T[i]) > 1:
        T1 = T.copy()
        T1[i] = T1[i][:-1]
    else:
        T1 = T[:i] + T[i + 1:]
    return [[i + 1, len(T[i])]] + CellOrder(T1)

def CandidateCells(P, J, c):
    i0, j0 = c
    C = set()
    for ip in range(i0, len(P)):
        if j0 <= len(J[ip]) and J[ip][j0] >= 0:
            C.add((ip, j0 + J[ip][j0]))
    return C

def ModifiedBackwardSlide(Tp, Jp, ck, c):
    i0, j0 = ck
    c1 = c
    Path = [c1]
    while c1 != ck:
        i, j = c1
        if i - 1 < 0:
            cp = [i, j - 1]
        elif j - 1 < 0:
            cp = [i - 1, j]
        else:
            if Tp[i - 1][j] > Tp[i][j - 1]:
                cp = [i - 1, j]
            else:
                cp = [i, j - 1]
        cvalue = Tp[i][j]
        Tp[i][j] = Tp[cp[0]][cp[1]]
        Tp[cp[0]][cp[1]] = cvalue
        c1 = cp
        Path.append(c1)
    return Tp, Code(Path)

def Code(Path):
    C = []
    for i in range(len(Path) - 1):
        if Path[i + 1][0] == Path[i][0] - 1:
            C.append('N')
        else:
            C.append('W')
    return list(reversed(C))

def CodeEntryL(E1, E2):
    if E1 == 'N':
        return E2 != 'N'
    if E1 == 0:
        return E2 == 'W'
    return False

def CodeLE(C1, C2):
    n = max(len(C1), len(C2))
    C11 = list(C1) + [0] * (n - len(C1))
    C21 = list(C2) + [0] * (n - len(C2))
    for i in range(n):
        if CodeEntryL(C11[i], C21[i]):
            return True
        if CodeEntryL(C21[i], C11[i]):
            return False
    return True

def isCodeMax(Codes, C):
    for D in Codes:
        if not CodeLE(D, C):
            return False
    return True

#-------------------------- The maps ---------------------------

def NPS(T):
    if isinstance(T, set):
        return {NPS(t) for t in T}
    n = sum(len(row) for row in T)
    P = T.copy()
    J = [[0] * len(row) for row in T]
    CO = CellOrder(T)
    for k in range(1, n + 1):
        i, j = CO[k - 1]
        Tem = ModifiedForwardSlide(P, CO[k - 1])
        P, ep = Tem
        ip, jp = ep
        J1 = [row.copy() for row in J]
        for h in range(i, ip):
            J1[h][j] = J[h + 1][j] - 1
        if ip < len(J1) and j < len(J1[ip]):
            J1[ip][j] = jp - j
        J = J1
    return [P, J]

def SPN(X):
    if isinstance(X, set):
        return {SPN(x) for x in X}
    P1, J1 = X
    CO = CellOrder(P1)
    n = sum(len(row) for row in P1)
    for k in range(n, 0, -1):
        Canidates = CandidateCells(P1, J1, CO[k - 1])
        Codes = set()
        CodesWithCells = set()
        for c in Canidates:
            Tem = ModifiedBackwardSlide(P1, J1, CO[k - 1], c)
            Codes.add(Tem[1])
            CodesWithCells.add((Tem[1], c))
