import numpy as np

def help_func(arg=None):
    if arg is None:
        print("How you dey? Na me dey ya side if you wan reason all of dis function so:\n"
                "1. VP\n"
                "2. InnProduct\n"
                "3. GramSchmidtOrthogonalisation\n"
                "4. LLLApp\n"
                "5. IntRel\n"
                "6. MinPoly\n"
                "7. LLL\n"
                "If you wan hear di gist about one function wey dey like that, abeg type help_func('function_name')\n"
                "As per example o, you fit type help_func('VP')\n")
    else:
        help_texts = {
            "VP": ("VP(v,u) : given two vectors of the same dimensions\n"
                   "u and v, returns their Euclidean inner product\n"
                   "Try InnPr([1,2],[5,6]): it should return: 17\n  "),
            "InnProduct": ("InnProduct(u,v) : Finds the inner product of u and v\n"
                           "according to the rule specified.The default here is\n"
                           "Euclidean but one can also change in a trivial\n"
                           "way to suit ones need."),
            "GramSchmidtOrthogonalisation": ("GramSchmidtOrthogonalisation(basis) : given independent vectors, basis, it \n"
                       "computes the orthogonal basis using Gram Schmidt\n"
                       " orthogonalization and parameters associated to it.\n"
                       " If you want to out put the orthogonal basis do : \n"
                       "GramSchmidtOrthogonalisation(basis)[3]\n  "),
            "LLLApp": ("LLLApp(basis,C) : The same as LLL(basis,C) but we don't use\n"
                       " Gauss elimination for independence here, since in most \n"
                       " applications we have real numbers and Gauss ellim. \n"
                       " is over rational field\n   "),
            "IntRel": ("IntRel(basis,C) : given a vector of real \n"
                       "numbers and a constant C, IntRel finds a vector\n"
                       "of integers which annihilates basis: a^T*b=0 \n"
                       "Try IntRel([1,Pi^2,Pi^4,Pi^6,Pi^8,V],10^15)\n"
                       "where\n V = Int(sqrt(x)*ln(x)^5/(1-x)^5,x=0..infinity)\n"
                       "should output :[0, 120, 140, -15, 0, 24,0.1*10^(-11)]\n  \n"
                       " more interesting example , try:\n"
                       "IntRel([a1,a2],10^15] , where\n"
                       "a1=Sum(1/n^3,n=1..infinity)\n"
                       "a2= Sum((-1)^(k+1)/k^3/binomial(2*k,k) ,k=1..infinity)\n"
                       " Output :[-2, 5, -.10e-213], [Zeta(3), 1/2*hypergeom([1, 1, 1, 1],\n"
                       "[2, 2, 3/2],-1/4)]\n  \n cool !  Apery's formula.\n"
                       "  \nEven More ! Try :  IntRel([c,d],10^15): where \n"
                       "c= Sum((-1)^n*n!^10*(205*n^2+250*n+77)/(2*n+1)!^5,n=0..infinity)\n"
                       "d= Sum(1/n^3,n=1..infinity)\n"
                       "to get :  [1,-64,0], [ c,d]\n"
                       "c and d as above.\n Amdberhan and Zeilberger's accelerating formula for zeta(3) !"),
            "MinPoly": ("If alpha is a real number, then \n"
                        "alpha is an algebraic number if for some r, the vector \n"
                        "[1,alpha,alph^2,...,alpha^r] has an integer relation\n"
                        "MinPoly(vect): given vect in the above form finds the\n"
                        "minimal polynomial for alpha.\n To write down your min. poly., set the vector product\n"
                        "of the first vec. less the last component with the second to\n"
                        " zero and replace alpha by x and write everything interms of x\n"
                        "Try MinPoly([1,sqrt(2),2]): it should return: \n"
                        "[-2,0,1,0],[1,sqrt(2),2]\n  "),
            "LLL": ("LLL(list) : given a list of independent vectors,(b[1],..,b[n])\n"
                    "returns the reduced linearly independent base vectors : \n"
                    "(b[1]*,..,b[n]*)\n Try:  LLL([1,2,3],[2,1,6],[1,5,7]), it should output :\n"
                    "[[-1, 1, 1], [2, 1, 2], [-1, -2, 1]]\n  ")
        }
        print(help_texts.get(arg, "No help available for this function"))

def vp(a, b):
    if len(a) != len(b):
        return "Error: the two vectors should have the same dimension"
    return np.dot(a, b)

def sp(c, w):
    return [c * wi for wi in w]

def vd(v, u):
    return [vi - ui for vi, ui in zip(v, u)]

def vs(v, u):
    return [vi + ui for vi, ui in zip(v, u)]

def GramSchmidtOrthogonalisation(basis):
    dim = len(basis)
    new_basis = [np.array(b) for b in basis]
    mu = np.zeros((dim, dim))
    B = np.zeros(dim)

    for i in range(dim):
        for j in range(i):
            mu[i, j] = vp(basis[i], new_basis[j]) / B[j]
            new_basis[i] = vd(new_basis[i], sp(mu[i, j], new_basis[j]))
        B[i] = vp(new_basis[i], new_basis[i])

    return mu, B, new_basis

def first_cond(k, l, mu, new_basis):
    if abs(mu[k, l]) > 0.5:
        q = int(np.floor(mu[k, l] + 0.5))
        new_basis[k] = vd(new_basis[k], sp(q, new_basis[l]))
        for j in range(l):
            mu[k, j] = mu[k, j] - q * mu[l, j]
        mu[k, l] = mu[k, l] - q
    return mu, new_basis

def second_cond(k, mu, B, new_basis):
    u_temp = mu[k, k-1]
    B_temp = B[k] + u_temp ** 2 * B[k-1]
    mu[k, k-1] = u_temp * B[k-1] / B_temp
    B[k] = B[k-1] * B[k] / B_temp
    B[k-1] = B_temp
    new_basis[k], new_basis[k-1] = new_basis[k-1], new_basis[k]
    for j in range(k-2):
        mu[k, j], mu[k-1, j] = mu[k-1, j], mu[k, j]
    for i in range(k+1, len(B)):
        u_prime = mu[i, k]
        mu[i, k] = mu[i, k-1] - u_temp * u_prime
        mu[i, k-1] = u_prime + mu[k, k-1] * mu[i, k]
    return mu, B, new_basis

def lll(basis):
    dim = len(basis)
    mu, B, new_basis = GramSchmidtOrthogonalisation(basis)
    k = 1
    while k < dim:
        mu, new_basis = first_cond(k, k-1, mu, new_basis)
        if B[k] < (3/4 - mu[k, k-1] ** 2) * B[k-1]:
            mu, B, new_basis = second_cond(k, mu, B, new_basis)
            if k > 1:
                k -= 1
        else:
            for l in range(k-2, -1, -1):
                mu, new_basis = first_cond(k, l, mu, new_basis)
            k += 1
    return new_basis

def lll_app(basis):
    dim = len(basis)
    mu, B, new_basis = GramSchmidtOrthogonalisation(basis)
    k = 1
    while k < dim:
        mu, new_basis = first_cond(k, k-1, mu, new_basis)
        if B[k] < (3/4 - mu[k, k-1] ** 2) * B[k-1]:
            mu, B, new_basis = second_cond(k, mu, B, new_basis)
            if k > 1:
                k -= 1
        else:
            for l in range(k-2, -1, -1):
                mu, new_basis = first_cond(k, l, mu, new_basis)
            k += 1
    return new_basis

def int_rel(basis, C):
    dim = len(basis)
    basis = [float(b) if isinstance(b, (int, float)) else b for b in basis]
    new_basis = []
    for i in range(dim):
        new_vec = [0] * i + [1] + [0] * (dim - i - 1) + [C * basis[i]]
        new_basis.append(new_vec)
    result = lll_app(new_basis)
    min_vec = min(result, key=lambda x: x[-1])
    return min_vec, basis

def min_poly(basis):
    return int_rel(basis, 10**15)