"""Build crystals, analyse symmetry, coordination and XRD with pymatgen (no API key needed)."""
import json
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pymatgen.core import Structure, Lattice
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from pymatgen.analysis.local_env import CrystalNN
from pymatgen.io.cif import CifWriter

structures = {
    "Si": Structure.from_spacegroup("Fd-3m", Lattice.cubic(5.431), ["Si"], [[0, 0, 0]]),
    "NaCl": Structure.from_spacegroup("Fm-3m", Lattice.cubic(5.640), ["Na", "Cl"], [[0, 0, 0], [0.5, 0.5, 0.5]]),
    "Cu": Structure.from_spacegroup("Fm-3m", Lattice.cubic(3.615), ["Cu"], [[0, 0, 0]]),
}

report = {}
fig, axes = plt.subplots(len(structures), 1, figsize=(7, 8), sharex=True)
for ax, (name, s) in zip(axes, structures.items()):
    sga = SpacegroupAnalyzer(s, symprec=1e-3)
    prim = sga.get_primitive_standard_structure()
    cnn = CrystalNN()
    cn = [cnn.get_cn(s, i) for i in range(len(s))]
    nn_dist = min(s.get_distance(0, j) for j in range(1, len(s))) if len(s) > 1 else None
    report[name] = dict(formula=s.composition.reduced_formula, spacegroup=sga.get_space_group_symbol(),
                        number=sga.get_space_group_number(), crystal_system=sga.get_crystal_system(),
                        atoms_conventional=len(s), atoms_primitive=len(prim),
                        density_g_cm3=round(s.density, 3), volume_A3=round(s.volume, 2),
                        coordination_numbers=sorted(set(cn)))
    CifWriter(s).write_file(f"{name}.cif")
    pat = XRDCalculator("CuKa").get_pattern(s, two_theta_range=(10, 90))
    ax.vlines(pat.x, 0, pat.y, lw=1.2); ax.set_ylabel(f"{name}\nI (a.u.)")
    top = np.argsort(pat.y)[::-1][:3]
    report[name]["top_xrd_peaks"] = [dict(two_theta=round(float(pat.x[i]), 2), hkl=str(pat.hkls[i][0]["hkl"])) for i in top]
axes[-1].set_xlabel("2 theta (deg), Cu K-alpha")
plt.tight_layout(); plt.savefig("xrd.png", dpi=200)

# supercell + vacancy + simple defect energy-free bookkeeping
sc = structures["Cu"] * (3, 3, 3)
sc.remove_sites([0])
report["Cu_vacancy_3x3x3"] = dict(atoms=len(sc), vacancy_concentration=round(1 / 108, 5))
json.dump(report, open("report.json", "w"), indent=2)
print(json.dumps(report, indent=2))
