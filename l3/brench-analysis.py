# Displays brench results as evidence that LVN actually optimizes programs

import matplotlib.pyplot as plt

data = []
with open("brench.out", "r") as file:
    next(file)
    for line in file:
        benchmark, run, result = line.strip().split(",")
        if result != "timeout":
            data.append((benchmark, run, int(result)))

benchmarks = list(sorted(set([entry[0] for entry in data])))
results_baseline = []
results_lvn = []
op = 0
total = 0

for benchmark in benchmarks:
    baseline_result = next(entry[2] for entry in data if entry[0] == benchmark and entry[1] == "baseline")
    lvn_result = next(entry[2] for entry in data if entry[0] == benchmark and entry[1] == "lvn")
    results_baseline.append(baseline_result)
    results_lvn.append(lvn_result)
    if baseline_result > lvn_result: op += 1
    total += 1

print(f"{op}/{total} benchmarks optimized")

'''
x = range(len(benchmarks))
plt.figure(figsize=(10, 6))

# plot baseline
plt.scatter(x, results_baseline, color="red", label="Baseline", zorder=2)
# plot lvn
plt.scatter(x, results_lvn, color="blue", label="LVN", zorder=2)

plt.xticks(x, benchmarks, rotation=45, ha="right")
plt.xlabel("Benchmarks")
plt.ylabel("Results")
plt.legend()
plt.grid(zorder=1, linestyle="--", alpha=0.6)

plt.ylim(0, 500)

plt.tight_layout()
plt.show()
'''
