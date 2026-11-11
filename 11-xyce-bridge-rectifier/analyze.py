"""Ripple and conduction analysis from Xyce output (.STEP produces concatenated CSV runs)."""
import pandas as pd, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import glob
files = sorted(glob.glob("bridge.csv*"))
fig, ax = plt.subplots(figsize=(8, 4.5))
for f in files:
    df = pd.read_csv(f)
    df.columns = [c.strip() for c in df.columns]
    steady = df[df["TIME"] > 0.06]                    # skip start-up
    vmax, vmin = steady["V(POS)"].max(), steady["V(POS)"].min()
    print(f"{f}: Vpeak={vmax:.2f} V, ripple={vmax-vmin:.2f} V pp, DC avg={steady['V(POS)'].mean():.2f} V")
    ax.plot(df["TIME"]*1e3, df["V(POS)"], label=f)
ax.set(xlabel="ms", ylabel="V(out) [V]", title="Bridge rectifier: ripple vs C"); ax.legend(); ax.grid(alpha=.3)
plt.savefig("ripple.png", dpi=200)
# theory: ripple ~ I/(2 f C) for full wave
I = 15/100
for C in (100e-6, 470e-6, 2200e-6): print(f"Theory C={C*1e6:.0f}uF: ripple ~ {I/(2*50*C):.2f} V")
