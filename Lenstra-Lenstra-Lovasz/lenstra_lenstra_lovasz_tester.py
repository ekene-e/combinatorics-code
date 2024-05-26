import lenstra_lenstra_lovasz as LLL
import numpy as np

def test_help_func():
    print("Testing help_func with no arguments")
    LLL.help_func()
    print("\nTesting help_func with 'VP' argument")
    LLL.help_func("VP")

def test_vp():
    print("\nTesting vp function")
    a = [1, 2]
    b = [5, 6]
    result = LLL.vp(a, b)
    print(f"vp({a}, {b}) = {result}")

def test_sp():
    print("\nTesting sp function")
    c = 3
    w = [1, 2, 3]
    result = LLL.sp(c, w)
    print(f"sp({c}, {w}) = {result}")

def test_vd():
    print("\nTesting vd function")
    v = [5, 6, 7]
    u = [1, 2, 3]
    result = LLL.vd(v, u)
    print(f"vd({v}, {u}) = {result}")

def test_vs():
    print("\nTesting vs function")
    v = [5, 6, 7]
    u = [1, 2, 3]
    result = LLL.vs(v, u)
    print(f"vs({v}, {u}) = {result}")

def test_GramSchmidtOrthogonalisation():
    print("\nTesting GramSchmidtOrthogonalisation function")
    basis = [[1, 2], [3, 4]]
    mu, B, new_basis = LLL.GramSchmidtOrthogonalisation(basis)
    print(f"GramSchmidtOrthogonalisation({basis}) = mu: {mu}, B: {B}, new_basis: {new_basis}")

def test_lll():
    print("\nTesting lll function")
    basis = [[1, 2, 3], [2, 1, 6], [1, 5, 7]]
    result = LLL.lll(basis)
    print(f"lll({basis}) = {result}")

def test_lll_app():
    print("\nTesting lll_app function")
    basis = [[1, 2, 3], [2, 1, 6], [1, 5, 7]]
    result = LLL.lll_app(basis)
    print(f"lll_app({basis}) = {result}")

def test_int_rel():
    print("\nTesting int_rel function")
    basis = [1, np.pi**2, np.pi**4, np.pi**6, np.pi**8]
    C = 10**15
    result, _ = LLL.int_rel(basis, C)
    print(f"int_rel({basis}, {C}) = {result}")

def test_min_poly():
    print("\nTesting min_poly function")
    basis = [1, np.sqrt(2), 2]
    result = LLL.min_poly(basis)
    print(f"min_poly({basis}) = {result}")

if __name__ == "__main__":
    test_help_func()
    test_vp()
    test_sp()
    test_vd()
    test_vs()
    test_GramSchmidtOrthogonalisation()
    test_lll()
    test_lll_app()
    test_int_rel()
    test_min_poly()