"""Compare FE tip deflection (beam.dat) with Euler-Bernoulli and Timoshenko solutions."""
import re
L, W, H, E, NU, P = 1000.0, 50.0, 50.0, 210e3, 0.3, 1000.0
I = W * H**3 / 12
eb = P * L**3 / (3 * E * I)
G = E / (2 * (1 + NU)); kappa = 5 / 6
tim = eb + P * L / (kappa * G * W * H)
uz = []
for line in open("beam.dat"):
    p = line.split()
    if len(p) == 4 and re.fullmatch(r"\d+", p[0]):
        uz.append(float(p[3]))
fe = sum(uz) / len(uz)
print(f"FE tip uz = {fe:.4f} mm | Euler-Bernoulli = {-eb:.4f} mm | Timoshenko = {-tim:.4f} mm")
print(f"Difference vs Timoshenko: {100*(fe+tim)/(-tim):+.2f} %")
