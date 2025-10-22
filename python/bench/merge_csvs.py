import sys, csv, glob, os

def main():
    if len(sys.argv) < 3:
        print("Usage: python merge_csvs.py OUT.csv file1.csv file2.csv ...")
        sys.exit(1)
    out = sys.argv[1]
    inputs = []
    for pat in sys.argv[2:]:
        inputs.extend(glob.glob(pat))
    if not inputs:
        print("No input files found.")
        sys.exit(1)

    rows = []
    header = None
    for f in inputs:
        with open(f, newline="") as fh:
            r = csv.reader(fh)
            h = next(r)
            if header is None:
                header = h
            for row in r:
                rows.append(row)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    print(f"Wrote {out} with {len(rows)} rows from {len(inputs)} files.")

if __name__ == "__main__":
    main()
