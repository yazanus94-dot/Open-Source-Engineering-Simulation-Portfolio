import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
DT_FS = 5.0
# g(r): last block of ave/time output (3 header lines, then per-frame blocks "idx nbins")
lines = open("rdf.dat").read().splitlines()[3:]
blocks, cur = [], []
for ln in lines:
    p = ln.split()
    if len(p) == 2 and p[1].isdigit() and int(p[1]) == 100:
        if cur: blocks.append(cur)
        cur = []
    elif len(p) == 3: cur.append([float(x) for x in p[1:]])
if cur: blocks.append(cur)
g = np.array(blocks[-1]); r, gr = g[:, 0], g[:, 1]
print(f"g(r) first peak: r = {r[gr.argmax()]:.2f} A, height = {gr.max():.2f} (liquid Ar: ~3.8 A, ~3)")

m = np.loadtxt("msd.dat", skiprows=1)
t = m[:, 0] * DT_FS                                  # fs
lo, hi = len(t) // 4, len(t)                         # fit diffusive regime
slope = np.polyfit(t[lo:hi], m[lo:hi, 1], 1)[0]      # A^2/fs
D = slope / 6 * 1e-20 / 1e-15                        # m^2/s (Einstein relation)
print(f"Self-diffusion coefficient D = {D:.2e} m^2/s  (exp. liquid Ar ~ 2e-9 m^2/s)")

fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].plot(r, gr); ax[0].set(xlabel="r (A)", ylabel="g(r)", title="Radial distribution function")
ax[1].plot(t / 1000, m[:, 1]); ax[1].set(xlabel="t (ps)", ylabel="MSD (A^2)", title=f"MSD, D = {D:.2e} m2/s")
plt.tight_layout(); plt.savefig("results.png", dpi=200)
