from typing import List, Tuple, Optional
import random

try:
    import numpy as np
except Exception:  
    np = None

Matrix = List[List[float]]

def gen_matrix(n: int, dtype: str = "float64", seed: Optional[int] = 42) -> Matrix:
    if seed is not None:
        random.seed(seed)
    if dtype not in ("float32", "float64"):
        raise ValueError("dtype must be 'float32' or 'float64'")
    scale = 1.0
    A: Matrix = [[(random.random() - 0.5) * 2 * scale for _ in range(n)] for _ in range(n)]
    return A

def zeros(n: int) -> Matrix:
    return [[0.0 for _ in range(n)] for _ in range(n)]

def naive_matmul(A: Matrix, B: Matrix) -> Matrix:
    n = len(A)
    C = zeros(n)
    for i in range(n):
        for k in range(n):
            aik = A[i][k]
            for j in range(n):
                C[i][j] += aik * B[k][j]
    return C

def blocked_matmul(A: Matrix, B: Matrix, block: int = 64) -> Matrix:
    n = len(A)
    C = zeros(n)
    for ii in range(0, n, block):
        for kk in range(0, n, block):
            for jj in range(0, n, block):
                i_max = min(ii + block, n)
                k_max = min(kk + block, n)
                j_max = min(jj + block, n)
                for i in range(ii, i_max):
                    for k in range(kk, k_max):
                        aik = A[i][k]
                        row_c = C[i]
                        row_bk = B[k]
                        for j in range(jj, j_max):
                            row_c[j] += aik * row_bk[j]
    return C

def numpy_dot(A: Matrix, B: Matrix) -> Matrix:
    if np is None:
        raise RuntimeError("NumPy not available")
    a = np.array(A, dtype=np.float64)
    b = np.array(B, dtype=np.float64)
    c = a @ b
    return c.tolist()

def fro_norm_diff(C: Matrix, D: Matrix) -> float:
    s = 0.0
    n = len(C)
    for i in range(n):
        for j in range(n):
            diff = C[i][j] - D[i][j]
            s += diff * diff
    return s ** 0.5
