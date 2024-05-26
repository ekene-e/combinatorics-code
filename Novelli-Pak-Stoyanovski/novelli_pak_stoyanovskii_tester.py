from novelli_pak_stoyanovski import (
    Perm2YT, YT, RandPerm, RandNPS, LowerOrderTableau, isStandard,
    ModifiedForwardSlide, CellOrder, CandidateCells, ModifiedBackwardSlide,
    Code, CodeEntryL, CodeLE, isCodeMax, NPS, SPN
)
import numpy as np

def test_Perm2YT():
    assert Perm2YT([1, 2, 3, 4], [2, 2]) == [[1, 2], [3, 4]]
    assert Perm2YT([1, 3, 2, 4], [2, 2]) == [[1, 3], [2, 4]]
    assert Perm2YT([1, 2, 3], [1, 2]) == [[1], [2, 3]]
    print("Perm2YT tests passed.")

def test_YT():
    result = YT([2, 2])
    expected = {
        ((2, 4), (1, 3)), ((3, 4), (1, 2)), ((2, 1), (3, 4)),
        ((4, 1), (2, 3)), ((4, 3), (2, 1)), ((1, 2), (3, 4)),
        ((1, 3), (2, 4)), ((4, 3), (1, 2)), ((1, 3), (4, 2)), 
        ((3, 2), (1, 4)), ((2, 3), (1, 4)), ((4, 1), (3, 2)),
        ((4, 2), (3, 1)), ((1, 4), (2, 3)), ((3, 1), (2, 4)),
        ((3, 1), (4, 2)), ((2, 1), (4, 3)), ((4, 2), (1, 3)),
        ((2, 3), (4, 1)), ((3, 2), (4, 1)), ((2, 4), (3, 1)),
        ((3, 4), (2, 1)), ((1, 2), (4, 3)), ((1, 4), (3, 2))
    }
    assert result == expected, f"Expected {expected}, but got {result}"
    print("YT tests passed.")


def test_RandPerm():
    assert len(RandPerm(5)) == 5
    assert len(set(RandPerm(5))) == 5
    print("RandPerm tests passed.")

def test_LowerOrderTableau():
    T = [[1, 2], [3, 4]]
    c = (1, 1)
    expected = np.array([[0, 0, 0], [0, 4, 0], [0, 0, 0]])
    result = LowerOrderTableau(T, c)
    assert (result == expected).all()
    print("LowerOrderTableau tests passed.")

def test_isStandard():
    M1 = np.array([[1, 2], [0, 3]])
    M2 = np.array([[1, 3], [0, 2]])
    assert isStandard(M1) == True
    assert isStandard(M2) == False
    print("isStandard tests passed.")

def test_ModifiedForwardSlide():
    T = [[1, 2], [3, 4]]
    c = (1, 1)
    result, end_point = ModifiedForwardSlide(T, c)
    expected = [[1, 2], [3, 4]]
    assert result == expected
    assert end_point == (1, 1)
    print("ModifiedForwardSlide tests passed.")

def test_CellOrder():
    T = [[1, 2], [3, 4]]
    result = CellOrder(T)
    expected = [[2, 2], [1, 2], [2, 1], [1, 1]]
    assert result == expected, f"Expected {expected}, but got {result}"
    print("CellOrder tests passed.")

def test_CandidateCells():
    P = [[1, 2], [3, 4]]
    J = [[0, 0], [0, 0]]
    c = (1, 1)
    result = CandidateCells(P, J, c)
    expected = {(1, 1)}
    assert result == expected
    print("CanidateCells tests passed.")

def test_ModifiedBackwardSlide():
    Tp = [[1, 2], [3, 4]]
    Jp = [[0, 0], [0, 0]]
    ck = (1, 1)
    c = (2, 2)
    result, path_code = ModifiedBackwardSlide(Tp, Jp, ck, c)
    expected = [[1, 4], [3, 2]]
    assert result == expected
    assert path_code == ['N']
    print("ModifiedBackwardSlide tests passed.")

def test_Code():
    Path = [(2, 2), (1, 2)]
    result = Code(Path)
    expected = ['N']
    assert result == expected
    print("Code tests passed.")

def test_CodeEntryL():
    assert CodeEntryL('N', 'W') == True
    assert CodeEntryL('W', 'N') == False
    print("CodeEntryL tests passed.")

def test_CodeLE():
    C1 = ['N', 'W']
    C2 = ['N', 'N']
    assert CodeLE(C1, C2) != True
    assert CodeLE(C2, C1) != False
    print("CodeLE tests passed.")

def test_isCodeMax():
    Codes = [['N', 'W'], ['N', 'N']]
    C = ['N', 'W']
    assert isCodeMax(Codes, C) != False
    print("isCodeMax tests passed.")

def test_NPS():
    T = [[1, 2], [3, 4]]
    P, J = NPS(T)
    expected_P = [[1, 2], [3, 4]]
    expected_J = [[0, 0], [0, 0]]
    assert P == expected_P, f"Expected {expected_P}, but got {P}"
    assert J == expected_J, f"Expected {expected_J}, but got {J}"
    print("NPS tests passed.")

if __name__ == "__main__":
    test_Perm2YT()
    test_YT()
    test_RandPerm()
    test_LowerOrderTableau()
    test_isStandard()
    test_ModifiedForwardSlide()
    test_CellOrder()
    test_CandidateCells()
    test_Code()
    test_CodeEntryL()
    test_CodeLE()
    test_isCodeMax()
    test_NPS()
    print("All tests passed.")
