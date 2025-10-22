package org.martyna.matmul;

import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

public class CLI {

    static class Args {
        int size = 256;
        String algo = "naive";
        int block = 64;
        int runs = 5;
        Long seed = 42L;
        String out = "../data/outputs/results_java.csv";
    }

    static Args parse(String[] argv) {
        Args a = new Args();
        for (int i = 0; i < argv.length; i++) {
            switch (argv[i]) {
                case "--size": a.size = Integer.parseInt(argv[++i]); break;
                case "--algo": a.algo = argv[++i]; break;
                case "--block": a.block = Integer.parseInt(argv[++i]); break;
                case "--runs": a.runs = Integer.parseInt(argv[++i]); break;
                case "--seed": a.seed = Long.parseLong(argv[++i]); break;
                case "--out": a.out = argv[++i]; break;
                default:
                    throw new IllegalArgumentException("Unknown arg: " + argv[i]);
            }
        }
        return a;
    }

    static double runOnce(int n, String algo, int block, long seed) {
        double[][] A = MatMul.randomMatrix(n, seed);
        double[][] B = MatMul.randomMatrix(n, seed + 1);
        long t0 = System.nanoTime();
        double[][] C;
        if ("naive".equals(algo)) {
            C = MatMul.naive(A, B);
        } else if ("blocked".equals(algo)) {
            C = MatMul.blocked(A, B, block);
        } else {
            throw new IllegalArgumentException("Unknown algo: " + algo);
        }
        long t1 = System.nanoTime();
        double ms = (t1 - t0) / 1e6;
        if (n <= 128) {
            // quick self-check: naive vs blocked on small n
            if ("blocked".equals(algo)) {
                double[][] ref = MatMul.naive(A, B);
                double err = MatMul.froNormDiff(C, ref);
                if (err > 1e-6 * n) throw new RuntimeException("Large error vs naive: " + err);
            }
        }
        return ms;
    }

    static void writeCsv(String out, List<String[]> rows) throws IOException {
        Path p = Path.of(out);
        Files.createDirectories(p.getParent());
        boolean exists = Files.exists(p);
        try (FileWriter fw = new FileWriter(out, true)) {
            if (!exists) {
                fw.write("timestamp,lang,algo,n,runs,block,mean_ms,stdev_ms,best_ms,est_GFLOP_s\n");
            }
            for (String[] r: rows) {
                fw.write(String.join(",", r));
                fw.write("\n");
            }
        }
    }

    public static void main(String[] argv) throws Exception {
        Args a = parse(argv);
        List<Double> times = new ArrayList<>();
        for (int r = 0; r < a.runs; r++) {
            times.add(runOnce(a.size, a.algo, a.block, (a.seed == null ? System.nanoTime() : a.seed + r)));
        }
        double mean = times.stream().mapToDouble(d->d).average().orElse(0.0);
        double stdev = 0.0;
        if (times.size() > 1) {
            double m = mean;
            double s = 0.0;
            for (double x: times) s += (x-m)*(x-m);
            stdev = Math.sqrt(s / times.size());
        }
        double best = times.stream().mapToDouble(d->d).min().orElse(mean);
        double gflops = (2.0 * Math.pow(a.size, 3)) / (mean/1000.0) / 1e9;

        List<String[]> rows = new ArrayList<>();
        rows.add(new String[] {
                Instant.now().toString(),
                "java", a.algo, String.valueOf(a.size), String.valueOf(a.runs),
                String.valueOf(a.block),
                String.format("%.3f", mean),
                String.format("%.3f", stdev),
                String.format("%.3f", best),
                String.format("%.3f", gflops)
        });
        writeCsv(a.out, rows);
        System.out.printf("[java] %s N=%d runs=%d block=%d -> mean=%.2f ms (σ=%.2f), best=%.2f ms, ~%.2f GFLOP/s%n",
                a.algo, a.size, a.runs, a.block, mean, stdev, best, gflops);
    }
}
