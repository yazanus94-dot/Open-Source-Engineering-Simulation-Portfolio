"""Li-ion cell simulation with PyBaMM: C-rate sweep (SPMe), model comparison (SPM/SPMe/DFN), temperature effect."""
import numpy as np
import pybamm
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

pv = pybamm.ParameterValues("Chen2020")


def discharge(model, c_rate, params=None):
    exp = pybamm.Experiment([f"Discharge at {c_rate} C until 2.5 V"])
    sim = pybamm.Simulation(model, parameter_values=params or pv, experiment=exp)
    return sim.solve()


# 1. C-rate sweep
fig, ax = plt.subplots(1, 3, figsize=(14, 4))
for c in [0.2, 0.5, 1, 2]:
    sol = discharge(pybamm.lithium_ion.SPMe(), c)
    q, v = sol["Discharge capacity [A.h]"].entries, sol["Terminal voltage [V]"].entries
    ax[0].plot(q, v, label=f"{c}C")
    print(f"{c}C: delivered {q[-1]:.3f} Ah")
ax[0].set(xlabel="Discharge capacity [Ah]", ylabel="Voltage [V]", title="C-rate sweep (SPMe)"); ax[0].legend()

# 2. Model fidelity vs cost
import time
for name, model in {"SPM": pybamm.lithium_ion.SPM(), "SPMe": pybamm.lithium_ion.SPMe(), "DFN": pybamm.lithium_ion.DFN()}.items():
    t0 = time.time(); sol = discharge(model, 1); dt = time.time() - t0
    ax[1].plot(sol["Time [min]"].entries, sol["Terminal voltage [V]"].entries, label=f"{name} ({dt:.1f}s)")
ax[1].set(xlabel="Time [min]", ylabel="Voltage [V]", title="Model comparison @1C"); ax[1].legend()

# 3. Temperature (lumped thermal) - ambient temperature sweep
for T in [0, 25, 40]:
    p = pv.copy(); p.update({"Ambient temperature [K]": 273.15 + T, "Initial temperature [K]": 273.15 + T})
    sol = discharge(pybamm.lithium_ion.SPMe({"thermal": "lumped"}), 1, p)
    ax[2].plot(sol["Time [min]"].entries, sol["Terminal voltage [V]"].entries, label=f"{T} C")
ax[2].set(xlabel="Time [min]", ylabel="Voltage [V]", title="Temperature @1C (SPMe+thermal)"); ax[2].legend()
plt.tight_layout(); plt.savefig("results.png", dpi=200)

# 4. Cycling with CC-CV charge and degradation (SEI growth)
model = pybamm.lithium_ion.SPMe({"SEI": "solvent-diffusion limited"})
cyc = pybamm.Experiment([("Discharge at 1C until 2.5 V", "Charge at 0.5C until 4.2 V", "Hold at 4.2 V until C/50")] * 20)
sim = pybamm.Simulation(model, parameter_values=pv, experiment=cyc)
sol = sim.solve()
cap = [c["Discharge capacity [A.h]"].entries[-1] - c["Discharge capacity [A.h]"].entries[0] for c in sol.cycles]
plt.figure(); plt.plot(range(1, len(cap) + 1), cap, "o-"); plt.xlabel("Cycle"); plt.ylabel("Discharge capacity [Ah]")
plt.title("Capacity fade from SEI growth"); plt.savefig("capacity_fade.png", dpi=200)
print("Capacity retention after 20 cycles: %.2f %%" % (100 * cap[-1] / cap[0]))
