#!/usr/bin/env python3
import os
import subprocess
import time
import statistics
import argparse
from pathlib import Path

def run_command(command, capture_output=False):
    """Runs a shell command and optionally captures its output."""
    try:
        if capture_output:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            return result.stdout.strip()
        else:
            subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}\n{e}")
        exit(1)

def measure_execution_time(command, num_runs):
    """Measures the average execution time over multiple runs."""
    times = []
    for _ in range(num_runs):
        start_time = time.time()
        subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        end_time = time.time()
        times.append(end_time - start_time)
    return statistics.mean(times)

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Benchmarking script with optimized and unoptimized runs.")
    parser.add_argument("--runs", type=int, default=1, help="Number of runs for each benchmark")
    args = parser.parse_args()

    benchmark_dir = Path("BenchmarkGame")
    llvm_prefix = run_command("brew --prefix llvm", capture_output=True)
    clang = f"{llvm_prefix}/bin/clang"
    opt = f"{llvm_prefix}/bin/opt"

    # Ensure build directory exists
    run_command("make -C build")

    # Store results
    results = []

    for c_file in benchmark_dir.glob("*.c"):
        c_file_name = c_file.name
        print(f"Processing {c_file.name}...")

        # Compile with LICM Pass
        licm_command = f"{clang} -fpass-plugin=build/licm/LICMPass.dylib {c_file}"
        run_command(licm_command, capture_output=True)

        # Generate LLVM IR for original and optimized versions
        ll_command = f"{clang} -S -emit-llvm -O0 -Xclang -disable-llvm-passes {c_file} -o a.ll"
        run_command(ll_command, capture_output=True)

        opt_command = f"{opt} -load-pass-plugin=build/licm/LICMPass.dylib -passes='mem2reg,LICMPass' a.ll -S > a_opt.ll"
        run_command(opt_command, capture_output=True)

        # Measure execution times
        original_time = measure_execution_time(f"{clang} -O0 a.ll && ./a.out", num_runs=args.runs)
        optimized_time = measure_execution_time(f"{clang} -O0 a_opt.ll && ./a.out", num_runs=args.runs)

        results.append((c_file_name, original_time, optimized_time))

    # Print results table
    print("\nResults:")
    print(f"{'Benchmark':<20}{'Original Time (s)':<20}{'Optimized Time (s)':<20}{'Improvement (%)':<15}")
    improvements = []
    for benchmark, original_time, optimized_time in results:
        improvement = ((original_time - optimized_time) / original_time) * 100 if original_time > 0 else 0
        improvements.append(improvement)
        print(f"{benchmark:<20}{original_time:<20.4f}{optimized_time:<20.4f}{improvement:<15.2f}")

    # Calculate and print mean improvement
    mean_improvement = statistics.mean(improvements) if improvements else 0
    print(f"\nMean Improvement: {mean_improvement:.2f}%")

if __name__ == "__main__":
    main()
