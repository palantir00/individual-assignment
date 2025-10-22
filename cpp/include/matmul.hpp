#pragma once
#include <vector>
#include <cstddef>

void matmul_naive(const std::vector<double>& A,
                  const std::vector<double>& B,
                  std::vector<double>& C,
                  int n);

void matmul_blocked(const std::vector<double>& A,
                    const std::vector<double>& B,
                    std::vector<double>& C,
                    int n,
                    int block);
