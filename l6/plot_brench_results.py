# Plots the overhead (% increase in instruction count) after
# doing the SSA round-trip conversion

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from statistics import mean

def compute_percentage(opt, baseline):
    result = abs(baseline - opt) / baseline
    return result


if __name__ == "__main__":
    data = []
    with open("brench.out", "r") as file:
        next(file)
        for line in file:
            benchmark, run, result = line.strip().split(",")
            if result != "timeout":
                data.append((benchmark, run, int(result)))

    # Sort the benchmarks by the name of the benchmark file
    benchmarks = list(sorted({benchmark for (benchmark, _, _) in data}))
    crude_results = []
    tdce_results = []

    for benchmark in benchmarks:
        baseline_result = next(
            result
            for (bench_name, run, result) in data
            if bench_name == benchmark and run == "baseline"
        )
        crude_roundtrip_result = next(
            result
            for (bench_name, run, result) in data
            if bench_name == benchmark and run == "crude-roundtrip"
        )
        tdce_roundtrip_result = next(
            result
            for (bench_name, run, result) in data
            if bench_name == benchmark and run == "tdce-roundtrip"
        )

        crude_results.append(compute_percentage(crude_roundtrip_result, baseline_result))
        tdce_results.append(compute_percentage(tdce_roundtrip_result, baseline_result))

    avg_crude_increase = round(mean(crude_results) * 100, 2)
    avg_tdce_increase = round(mean(tdce_results) * 100, 2)
    print("Mean increase in instruction count:")
    print(f'Crude roundtrip: {avg_crude_increase}%')
    print(f'TCDE roundtrip: {avg_tdce_increase}%')

    x = range(len(benchmarks))
    plt.figure(figsize=(10, 6))

    plt.scatter(x, crude_results, color="red", label="Crude round-trip", zorder=2)
    plt.scatter(x, tdce_results, color="green", label="TDCE round trip", zorder=2) 

    plt.title(
        "Percentage increase in instruction count after SSA round trip (lower is better)"
    )
    plt.xticks(x, benchmarks, rotation=45, ha="right")

    # Display y-axis as double-digit percentages
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))

    plt.xlabel("Benchmarks")
    plt.ylabel("Percentage")
    plt.legend()
    plt.grid(zorder=1, linestyle="--", alpha=0.6)

    plot_filename = "plot.png"

    plt.tight_layout()
    plt.savefig(plot_filename)
    print(f'Plot saved in {plot_filename}')
    plt.close()
