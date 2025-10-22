#include "matmul.hpp"

void matmul_naive(const std::vector<double>& A,
                  const std::vector<double>& B,
                  std::vector<double>& C,
                  int n) {
    for (int i = 0; i < n; ++i) {
        for (int k = 0; k < n; ++k) {
            double aik = A[i * n + k];
            for (int j = 0; j < n; ++j) {
                C[i * n + j] += aik * B[k * n + j];
            }
        }
    }
}

void matmul_blocked(const std::vector<double>& A,
                    const std::vector<double>& B,
                    std::vector<double>& C,
                    int n,
                    int block) {
    for (int ii = 0; ii < n; ii += block) {
        for (int kk = 0; kk < n; kk += block) {
            for (int jj = 0; jj < n; jj += block) {
                int imax = std::min(ii + block, n);
                int kmax = std::min(kk + block, n);
                int jmax = std::min(jj + block, n);
                for (int i = ii; i < imax; ++i) {
                    for (int k = kk; k < kmax; ++k) {
                        double aik = A[i * n + k];
                        for (int j = jj; j < jmax; ++j) {
                            C[i * n + j] += aik * B[k * n + j];
                        }
                    }
                }
            }
        }
    }
}
