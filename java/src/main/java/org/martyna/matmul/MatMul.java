package org.martyna.matmul;

import java.util.Random;

public class MatMul {

    public static double[][] randomMatrix(int n, long seed) {
        Random rnd = new Random(seed);
        double[][] a = new double[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                a[i][j] = (rnd.nextDouble() - 0.5) * 2.0;
            }
        }
        return a;
    }

    public static double[][] zeros(int n) {
        double[][] c = new double[n][n];
        return c;
    }

    public static double[][] naive(double[][] A, double[][] B) {
        int n = A.length;
        double[][] C = zeros(n);
        for (int i = 0; i < n; i++) {
            for (int k = 0; k < n; k++) {
                double aik = A[i][k];
                double[] rowB = B[k];
                double[] rowC = C[i];
                for (int j = 0; j < n; j++) {
                    rowC[j] += aik * rowB[j];
                }
            }
        }
        return C;
    }

    public static double[][] blocked(double[][] A, double[][] B, int block) {
        int n = A.length;
        double[][] C = zeros(n);
        for (int ii = 0; ii < n; ii += block) {
            for (int kk = 0; kk < n; kk += block) {
                for (int jj = 0; jj < n; jj += block) {
                    int imax = Math.min(ii + block, n);
                    int kmax = Math.min(kk + block, n);
                    int jmax = Math.min(jj + block, n);
                    for (int i = ii; i < imax; i++) {
                        double[] rowC = C[i];
                        for (int k = kk; k < kmax; k++) {
                            double aik = A[i][k];
                            double[] rowB = B[k];
                            for (int j = jj; j < jmax; j++) {
                                rowC[j] += aik * rowB[j];
                            }
                        }
                    }
                }
            }
        }
        return C;
    }

    public static double froNormDiff(double[][] C, double[][] D) {
        int n = C.length;
        double s = 0.0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                double diff = C[i][j] - D[i][j];
                s += diff * diff;
            }
        }
        return Math.sqrt(s);
    }
}
