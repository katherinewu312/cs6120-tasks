# Plots the overhead (% increase in instruction count) after
# doing the SSA round-trip conversion

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


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
    results = []

    for benchmark in benchmarks:
        baseline_result = next(
            result
            for (bench_name, run, result) in data
            if bench_name == benchmark and run == "baseline"
        )
        roundtrip_result = next(
            result
            for (bench_name, run, result) in data
            if bench_name == benchmark and run == "crude-roundtrip"
        )

        results.append(compute_percentage(roundtrip_result, baseline_result))

    x = range(len(benchmarks))
    plt.figure(figsize=(10, 6))

    plt.scatter(x, results, color="green")

    plt.title(
        "Percentage increase in instruction count after SSA round trip (lower is better)"
    )
    plt.xticks(x, benchmarks, rotation=45, ha="right")

    # Display y-axis as double-digit percentages
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))

    plt.xlabel("Benchmarks")
    plt.ylabel("Percentage")
    plt.grid(zorder=1, linestyle="--", alpha=0.6)

    plt.tight_layout()
    plt.savefig("plot.png")
    plt.close()
