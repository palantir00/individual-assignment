package org.martyna.matmul;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class MatMulTest {

    @Test
    public void testSmallCorrectness() {
        int n = 8;
        double[][] A = MatMul.randomMatrix(n, 1);
        double[][] B = MatMul.randomMatrix(n, 2);
        double[][] Cn = MatMul.naive(A, B);
        double[][] Cb = MatMul.blocked(A, B, 4);
        double err = MatMul.froNormDiff(Cn, Cb);
        assertTrue(err < 1e-6 * n, "Blocked should match Naive (err=" + err + ")");
    }
}
