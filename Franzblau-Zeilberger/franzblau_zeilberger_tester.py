import franzblau_zeilberger as fz
import _testinternalcapi

def print_tableau(label, tableau):
    print(f"{label}:")
    for row in tableau:
        print(row)
    print()

def test_chop():
    print("Testing Chop...")
    lam = [5, 3, 2, 1, 0]
    result = fz.Chop(lam)
    expected = [5, 3, 2, 1]
    print(f"Input: {lam}, Result: {result}, Expected: {expected}")
    assert result == expected

def test_bad_elem():
    print("Testing BadElem...")
    T = [[1, 8, 12], [4, 5], [3, 7], [6]]
    result = fz.BadElem(T)
    expected = [3, 3, 1]
    print(f"Input: {T}, Result: {result}, Expected: {expected}")
    assert result == expected

def test_satisfy_dc():
    print("Testing SatisfyDC...")
    T = [[1, 2, 3], [4, 5], [6]]
    d = ['C1', 'C1', 'C2']
    result = fz.SatisfyDC(T, d)
    print(f"Input: {T}, {d}, Result: {result}")

def test_build_s():
    print("Testing BuildS...")
    d = [['C1'], ['C2'], ['R2']]
    S = [['C1', 'C3'], ['C1']]
    result = fz.BuildS(d, S)
    expected = [['C1', 'C1', 'C3'], ['C2', 'C1'], ['R2']]
    print(f"Input: {d}, {S}, Result: {result}, Expected: {expected}")
    assert result == expected

def test_transpose():
    print("Testing Transpose...")
    YT = [[1, 2], [3]]
    result = fz.Transpose(YT)
    expected = [[1, 3], [2]]
    print(f"Input: {YT}, Result: {result}, Expected: {expected}")
    assert result == expected

def test_insert1():
    print("Testing INSERT1...")
    T = [[1, 2, 4], [5, 6]]
    aj = 3
    j = 1
    result = fz.INSERT1(aj, j, T)
    expected = ([[1, 2, 3, 4], [5, 6]], 3)
    print(f"Input: {aj}, {j}, {T}, Result: {result}, Expected: {expected}")
    assert result == expected

def test_remove1():
    print("Testing REMOVE1...")
    T = [[1, 2, 3, 4], [5, 6]]
    i = 1
    j = 3
    result = fz.REMOVE1(i, j, T)
    expected = [[1, 2, 4], [5, 6]]
    print(f"Input: {i}, {j}, {T}, Result: {result}, Expected: {expected}")
    assert result == expected

def test_simplify1():
    print("Testing SIMPLIFY1...")
    T = [[1, 2], [], [3]]
    result = fz.SIMPLIFY1(T)
    expected = [[1, 2], [3]]
    print(f"Input: {T}, Result: {result}, Expected: {expected}")
    assert result == expected

def test_exchange2():
    print("Testing EXCHANGE2...")
    T = [[1, 2], [3, 4]]
    i1, j1 = 1, 1
    i2, j2 = 2, 2
    result = fz.EXCHANGE2(i1, j1, i2, j2, T)
    expected = ([[2, 4], [1, 3]], 1, 2)
    print(f"Input: {i1}, {j1}, {i2}, {j2}, {T}, Result: {result}, Expected: {expected}")
    assert result == expected

def test_rsor_findr():
    print("Testing RSORT and FINDR...")
    YT = [
        [1, 2, 3],
        [4, 5],
        [6]
    ]
    print_tableau("Initial Young Tableau (YT)", YT)
    PYT = fz.RSORT(YT)
    T, S = PYT
    print_tableau("Standard Young Tableau (T)", T)
    print_tableau("Pointer Tableau (S)", S)
    YT_reconstructed = fz.FINDR(T, S)
    print_tableau("Reconstructed Young Tableau (YT)", YT_reconstructed)
    assert YT == YT_reconstructed

def run_tests():
    test_chop()
    test_bad_elem()
    test_satisfy_dc()
    test_build_s()
    test_transpose()
    test_insert1()
    test_remove1()
    test_simplify1()
    test_exchange2()
    test_rsor_findr()

if __name__ == "__main__":
    run_tests()
    print("All tests completed.")
