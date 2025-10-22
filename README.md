# Matrix Multiplication Benchmark (Java / Python / C++)

## Project Overview
This repository contains an individual assignment focused on implementing and benchmarking **dense matrix multiplication** across three programming languages — **Python, Java, and C++**.  
The goal is to analyze the performance impact of:
- Programming language execution model (interpreted vs compiled),
- Algorithmic design (naive vs cache-blocked),
- Dataset size and parameterization,
- Profiling and benchmarking methodology.

All experiments follow the same structure and output format to ensure full reproducibility and comparability.

---

## Repository Structure
individual-assignment/
│
├── latex/                 # LaTeX report + compiled PDF
│   ├── main.tex
│   └── main.pdf
│
├── data/
│   ├── inputs/            # Input data (if any)
│   └── outputs/           # Benchmark results (.csv)
│
├── python/                # Python implementation
│   ├── matmul/matmul_prod.py   # Algorithms (naive & blocked)
│   ├── bench/bench.py          # Benchmark runner
│   └── bench/merge_csvs.py     # Combine multiple CSVs
│
├── java/                  # Java (Maven) implementation
│   ├── src/main/java/org/martyna/matmul/
│   │   ├── MatMul.java    # Algorithms
│   │   └── CLI.java       # Benchmark runner
│   └── src/test/java/...  # Unit tests
│
├── cpp/                   # C++ (CMake) implementation
│   ├── include/matmul.hpp
│   ├── src/matmul.cpp     # Algorithms
│   └── src/bench.cpp      # Benchmark runner
│
└── README.md              # Project documentation 


---

## Quick Start

### Requirements
Install the following tools:
- **Python 3.10+**
- **JDK 17+**
- **Maven**
- **CMake** + C++ compiler (Clang or GCC)
- *(Optional)* **LaTeX / Overleaf** for compiling the report

If you're on macOS, install everything via Homebrew:
```bash
brew install python cmake maven temurin@17 

**Python Benchmarks**
cd python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m bench.bench --size 128 --algo naive --runs 3 --out ../data/outputs/results_py.csv
python -m bench.bench --size 128 --algo blocked --block 64 --runs 3 --out ../data/outputs/results_py.csv

**Java Benchmarks**
cd ../java
mvn -q test
mvn -q -DskipTests exec:java -Dexec.mainClass=org.martyna.matmul.CLI -Dexec.args="--size 128 --algo naive --runs 3 --out ../data/outputs/results_java.csv"
mvn -q -DskipTests exec:java -Dexec.mainClass=org.martyna.matmul.CLI -Dexec.args="--size 128 --algo blocked --block 64 --runs 3 --out ../data/outputs/results_java.csv"

**C++ Benchmarks**
cd ../cpp
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
./build/matmul_bench --size 128 --algo naive   --runs 3 --out ../data/outputs/results_cpp.csv
./build/matmul_bench --size 128 --algo blocked --block 64 --runs 3 --out ../data/outputs/results_cpp.csv

**Merge All Results**
cd ../python
python -m bench.merge_csvs ../data/outputs/results_all.csv ../data/outputs/*.csv

## Profiling Tools

Example profiling commands used in the study:

**Python:**
```bash
python -m cProfile -o profile_py.prof bench/bench.py --size 512 --algo blocked --runs 3
**Java**
java -XX:StartFlightRecording=filename=java.jfr,duration=30s \
     -cp target/classes org.martyna.matmul.CLI --size 512 --algo blocked --runs 3
**C++:**
perf record ./build/matmul_bench --size 512 --algo blocked --runs 3
valgrind --tool=callgrind ./build/matmul_bench --size 512 --algo blocked --runs 3

## Reproducibility

All code, data, and this report are available in this repository.  
To reproduce the results:

1. Clone the repository  
2. Run benchmarks for Python, Java, and C++  
3. Merge the CSV files  
4. Compile the report using LaTeX or Overleaf  

The experiment was executed under identical conditions to ensure consistency across runs.

---

## Author

**Martyna Chmielińska**  
Polish-Japanese Academy of Information Technology (PJATK)  
*Individual Assignment – Performance Benchmarking and Profiling*
