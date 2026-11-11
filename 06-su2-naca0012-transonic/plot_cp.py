import pandas as pd, matplotlib.pyplot as plt
df = pd.read_csv("surface_flow.csv"); df.columns = [c.strip().strip('"') for c in df.columns]
df = df.sort_values("x")
plt.plot(df["x"], -df["Pressure_Coefficient"], ".", ms=3)
plt.xlabel("x/c"); plt.ylabel("-Cp"); plt.title("NACA0012 M=0.8 AoA=1.25 (Euler)"); plt.grid(alpha=.3)
plt.savefig("cp.png", dpi=200)
