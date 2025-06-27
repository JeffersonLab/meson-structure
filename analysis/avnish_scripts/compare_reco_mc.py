import pandas as pd
import matplotlib.pyplot as plt

# Load CSV data
filename = "/home/ubuntu/meson-structure/data/csv_files_kaon/k_lambda_5x41_5000evt_001.reco_dis.csv/volatile/eic/romanov/meson-structure-2025-06/reco/k_lambda_5x41_5000evt_001.reco_dis.csv"  # Replace with your actual CSV file
df = pd.read_csv(filename)

# Define kinematic quantities to compare
quantities = ["x", "q2", "y", "nu", "w"]
methods = ["da", "esigma", "electron", "jb", "ml", "sigma", "mc"]

# Plot comparisons
for q in quantities:
    plt.figure(figsize=(10, 6))
    for method in methods:
        col = f"{method}_{q}"
        if col in df.columns:
            plt.plot(df["evt"], df[col], label=method)

    plt.title(f"Comparison of different methods for {q.upper()}")
    plt.xlabel("Event")
    plt.ylabel(q.upper())
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # plt.savefig(f"compare_{q}.png")  # Save plot
    plt.show()
