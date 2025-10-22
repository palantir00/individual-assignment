#include "matmul.hpp"
#include <random>
#include <chrono>
#include <string>
#include <iostream>
#include <fstream>
#include <filesystem>
#include <cmath>

struct Args {
    int size = 256;
    std::string algo = "naive";
    int block = 64;
    int runs = 5;
    long long seed = 42;
    std::string out = "../data/outputs/results_cpp.csv";
};

Args parse(int argc, char** argv) {
    Args a;
    for (int i = 1; i < argc; ++i) {
        std::string s(argv[i]);
        if (s == "--size") a.size = std::stoi(argv[++i]);
        else if (s == "--algo") a.algo = argv[++i];
        else if (s == "--block") a.block = std::stoi(argv[++i]);
        else if (s == "--runs") a.runs = std::stoi(argv[++i]);
        else if (s == "--seed") a.seed = std::stoll(argv[++i]);
        else if (s == "--out") a.out = argv[++i];
        else {
            throw std::runtime_error("Unknown arg: " + s);
        }
    }
    return a;
}

static std::vector<double> random_matrix(int n, long long seed) {
    std::mt19937_64 rng(seed);
    std::uniform_real_distribution<double> dist(-1.0, 1.0);
    std::vector<double> A(n * n);
    for (auto &x : A) x = dist(rng);
    return A;
}

double fro_norm_diff(const std::vector<double>& C, const std::vector<double>& D, int n) {
    long double s = 0.0L;
    for (int i = 0; i < n*n; ++i) {
        long double diff = (long double)C[i] - (long double)D[i];
        s += diff * diff;
    }
    return std::sqrt((double)s);
}

int main(int argc, char** argv) {
    Args a = parse(argc, argv);

    std::vector<double> times;
    times.reserve(a.runs);

    for (int r = 0; r < a.runs; ++r) {
        auto A = random_matrix(a.size, a.seed + r);
        auto B = random_matrix(a.size, a.seed + r + 1);
        std::vector<double> C(a.size * a.size, 0.0);

        auto t0 = std::chrono::high_resolution_clock::now();
        if (a.algo == "naive") {
            matmul_naive(A, B, C, a.size);
        } else if (a.algo == "blocked") {
            matmul_blocked(A, B, C, a.size, a.block);
        } else {
            throw std::runtime_error("Unknown algo");
        }
        auto t1 = std::chrono::high_resolution_clock::now();
        double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();

        if (a.size <= 128 && a.algo == "blocked") {
            std::vector<double> Cref(a.size * a.size, 0.0);
            matmul_naive(A, B, Cref, a.size);
            double err = fro_norm_diff(C, Cref, a.size);
            if (err > 1e-6 * a.size) {
                std::cerr << "Large error vs naive: " << err << "\n";
                return 2;
            }
        }
        times.push_back(ms);
    }

    double mean = 0.0;
    for (double x: times) mean += x;
    mean /= times.size();
    double var = 0.0;
    for (double x: times) { double d = x - mean; var += d*d; }
    var /= times.size();
    double stdev = std::sqrt(var);
    double best = *std::min_element(times.begin(), times.end());
    double gflops = (2.0 * (double)a.size * a.size * a.size) / (mean / 1000.0) / 1e9;

    std::filesystem::create_directories(std::filesystem::path(a.out).parent_path());
    bool exists = std::filesystem::exists(a.out);
    std::ofstream out(a.out, std::ios::app);
    if (!exists) {
        out << "timestamp,lang,algo,n,runs,block,mean_ms,stdev_ms,best_ms,est_GFLOP_s\n";
    }
    out << std::chrono::system_clock::to_time_t(std::chrono::system_clock::now())
        << ",cpp," << a.algo << "," << a.size << "," << a.runs << "," << a.block
        << "," << mean << "," << stdev << "," << best << "," << gflops << "\n";

    std::cout << "[cpp] " << a.algo << " N=" << a.size << " runs=" << a.runs << " block=" << a.block
              << " -> mean=" << mean << " ms (σ=" << stdev << "), best=" << best
              << " ms, ~" << gflops << " GFLOP/s\n";
    return 0;
}
