import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
ac = np.loadtxt("ac_out.csv"); f = ac[:, 0]
fig, ax = plt.subplots(2, 2, figsize=(11, 7))
ax[0, 0].semilogx(f, ac[:, 1]); ax[0, 0].set(title="Magnitude", xlabel="Hz", ylabel="dB"); ax[0, 0].grid(True, which="both", alpha=.3)
ax[1, 0].semilogx(f, ac[:, 3]); ax[1, 0].set(title="Phase", xlabel="Hz", ylabel="deg"); ax[1, 0].grid(True, which="both", alpha=.3)
t = np.loadtxt("tran_out.csv"); ax[0, 1].plot(t[:, 0]*1e3, t[:, 1], t[:, 0]*1e3, t[:, 3]); ax[0, 1].set(title="RLC step response (ringing)", xlabel="ms")
c = np.loadtxt("clipper_out.csv"); ax[1, 1].plot(c[:, 0]*1e3, c[:, 1], c[:, 0]*1e3, c[:, 3]); ax[1, 1].set(title="Diode clipper", xlabel="ms")
plt.tight_layout(); plt.savefig("results.png", dpi=200)
# analytic cross-check
L, C, R = 10e-3, 100e-9, 50.0
f0 = 1/(2*np.pi*np.sqrt(L*C)); Q = np.sqrt(L/C)/R
print(f"Analytic f0 = {f0:.1f} Hz, Q = {Q:.2f}, peak = {20*np.log10(Q):.2f} dB; simulated peak = {ac[:,1].max():.2f} dB @ {f[ac[:,1].argmax()]:.0f} Hz")
