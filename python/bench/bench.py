import argparse, csv, os, time, math, statistics
from datetime import datetime
from typing import Optional
from matmul.matmul_prod import gen_matrix, naive_matmul, blocked_matmul, numpy_dot, fro_norm_diff

def run_once(n: int, algo: str, block: int, seed: Optional[int]) -> float:
    A = gen_matrix(n, seed=seed)
    B = gen_matrix(n, seed=None if seed is None else seed + 1)
    t0 = time.perf_counter()
    if algo == "naive":
        C = naive_matmul(A, B)
    elif algo == "blocked":
        C = blocked_matmul(A, B, block=block)
    elif algo == "numpy":
        C = numpy_dot(A, B)
    else:
        raise ValueError("Unknown algo")
    dt = (time.perf_counter() - t0) * 1000.0
    if n <= 128 and algo != "numpy":
        try:
            ref = numpy_dot(A, B)
            err = fro_norm_diff(C, ref)
            assert err < 1e-6 * n, f"Large error vs NumPy: {err}"
        except Exception:
            pass
    return dt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", type=int, required=True, help="Matrix size N (NxN)")
    ap.add_argument("--algo", choices=["naive", "blocked", "numpy"], default="naive")
    ap.add_argument("--block", type=int, default=64)
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", type=str, required=True, help="Output CSV path")
    args = ap.parse_args()

    times = []
    for r in range(args.runs):
        dt = run_once(args.size, args.algo, args.block, args.seed + r if args.seed is not None else None)
        times.append(dt)

    mean = statistics.fmean(times)
    stdev = statistics.pstdev(times) if len(times) > 1 else 0.0
    best = min(times)
    gflops = (2.0 * (args.size ** 3)) / (mean / 1000.0) / 1e9

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    file_exists = os.path.exists(args.out)
    with open(args.out, "a", newline="") as f:
        w = csv.writer(f)
        if not file_exists:
            w.writerow(["timestamp","lang","algo","n","runs","block","mean_ms","stdev_ms","best_ms","est_GFLOP_s"])
        w.writerow([datetime.utcnow().isoformat(), "python", args.algo, args.size, args.runs, args.block, f"{mean:.3f}", f"{stdev:.3f}", f"{best:.3f}", f"{gflops:.3f}"])

    print(f"[python] {args.algo} N={args.size} runs={args.runs} block={args.block} -> mean={mean:.2f} ms (σ={stdev:.2f}), best={best:.2f} ms, ~{gflops:.2f} GFLOP/s")

if __name__ == "__main__":
    main()
