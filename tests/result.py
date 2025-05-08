import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the CSV
df = pd.read_csv("perf.csv")

print(df)

# 3. Plot Avg Latency vs Concurrency
plt.figure()
plt.plot(df["Concurrency"], df["Avg Latency"], marker="o")
plt.title("Average Latency vs Concurrency")
plt.xlabel("Number of Concurrent Requests")
plt.ylabel("Average Latency (s)")
plt.grid(True)
plt.tight_layout()
plt.savefig("avg_latency.png")
plt.show()

# 4. Plot P95 Latency vs Concurrency
plt.figure()
plt.plot(df["Concurrency"], df["P95 Latency"], marker="o")
plt.title("95th-Percentile Latency vs Concurrency")
plt.xlabel("Number of Concurrent Requests")
plt.ylabel("P95 Latency (s)")
plt.grid(True)
plt.tight_layout()
plt.savefig("p95_latency.png")
plt.show()
