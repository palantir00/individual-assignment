import csv, sys, math

def main(inp, outp):
    rows = []
    with open(inp, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append(row)

    rows.sort(key=lambda x: (int(x["n"]), x["lang"], x["algo"]))

    def fmt(x, digits=1):
        try:
            return f"{float(x):.{digits}f}"
        except:
            return x

    lines = []
    lines.append(r"\begin{table}[h]")
    lines.append(r"\centering")
    lines.append(r"\begin{tabular}{l l r r r r r r}")
    lines.append(r"\toprule")
    lines.append(r"Lang & Algo & $N$ & Runs & Block & Mean [ms] & Best [ms] & GFLOP/s \\")
    lines.append(r"\midrule")
    for row in rows:
        lines.append(
            f"{row['lang']} & {row['algo']} & {row['n']} & {row['runs']} & {row['block']} & "
            f"{fmt(row['mean_ms'],1)} & {fmt(row['best_ms'],1)} & {fmt(row['est_GFLOP_s'],2)} \\\\"
        )
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\caption{Zbiorcze wyniki benchmarków (średnia z wielu uruchomień).}")
    lines.append(r"\label{tab:results}")
    lines.append(r"\end{table}")

    with open(outp, "w") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python csv_to_latex.py INPUT.csv OUTPUT.tex")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
