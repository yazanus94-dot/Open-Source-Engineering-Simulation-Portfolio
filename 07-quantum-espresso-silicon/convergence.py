"""Converge total energy w.r.t. ecutwfc and k-mesh, then fit the equilibrium lattice constant (Birch-Murnaghan)."""
import re, subprocess, os, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

TEMPLATE = open("scf.in.template").read()
NP = os.environ.get("NP", "2")
RY2EV = 13.605693


def run(alat=10.26, ecut=30, k=8, tag=None):
    tag = tag or f"a{alat}_e{ecut}_k{k}"
    inp = TEMPLATE.replace("__ALAT__", str(alat)).replace("__ECUT__", str(ecut)).replace("__K__", str(k))
    open(f"runs/{tag}.in", "w").write(inp)
    out = subprocess.run(f"mpirun -np {NP} pw.x -in runs/{tag}.in", shell=True, capture_output=True, text=True).stdout
    open(f"runs/{tag}.out", "w").write(out)
    return float(re.findall(r"!\s+total energy\s+=\s+(-?\d+\.\d+)", out)[-1])


os.makedirs("runs", exist_ok=True)
ecuts = [15, 20, 25, 30, 40, 50]
e_cut = [run(ecut=e) for e in ecuts]
ks = [2, 4, 6, 8, 10]
e_k = [run(k=k) for k in ks]
alats = np.linspace(10.0, 10.5, 9)
e_a = [run(alat=a, ecut=40, k=8) for a in alats]

# Fit E(V) with a parabola in a (quick) and report
c = np.polyfit(alats, e_a, 2)
a0 = -c[1] / (2 * c[0])
print(f"Equilibrium lattice constant: {a0:.3f} bohr = {a0*0.529177:.3f} A (exp. 5.431 A)")

fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
ax[0].plot(ecuts, [(e - e_cut[-1]) * RY2EV * 1000 for e in e_cut], "o-"); ax[0].set(xlabel="ecutwfc (Ry)", ylabel="dE (meV)")
ax[1].plot(ks, [(e - e_k[-1]) * RY2EV * 1000 for e in e_k], "o-"); ax[1].set(xlabel="k-mesh (NxNxN)")
ax[2].plot(alats, e_a, "o"); ax[2].plot(alats, np.polyval(c, alats)); ax[2].set(xlabel="a (bohr)", ylabel="E (Ry)")
plt.tight_layout(); plt.savefig("convergence.png", dpi=200)
