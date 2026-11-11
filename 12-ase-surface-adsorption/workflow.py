"""ASE workflow with the EMT calculator (fast, no external code):
   1) Equation of state -> lattice constant and bulk modulus of Cu
   2) Cu(111) slab relaxation with fixed bottom layers
   3) Adsorption energies of Au at fcc/hcp/ontop/bridge sites
   Swap EMT for GPAW / QE / VASP by changing one line."""
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from ase.build import bulk, fcc111, add_adsorbate
from ase.calculators.emt import EMT
from ase.constraints import FixAtoms
from ase.optimize import BFGS
from ase.eos import EquationOfState
from ase.io import write, read
from ase.units import GPa

# 1. EOS
cu = bulk("Cu", "fcc", a=3.6, cubic=True)
cu.calc = EMT()
cell0, vols, es = cu.get_cell(), [], []
for s in np.linspace(0.97, 1.03, 9):
    a = cu.copy(); a.set_cell(cell0 * s, scale_atoms=True); a.calc = EMT()
    vols.append(a.get_volume()); es.append(a.get_potential_energy())
v0, e0, B = EquationOfState(vols, es, eos="birchmurnaghan").fit()
a0 = v0 ** (1 / 3)   # cubic cell: V = a^3
print(f"Cu: a0 = {a0:.3f} A (exp 3.615), B = {B/GPa:.1f} GPa (exp 140)")

# 2/3. slab + adsorbates
def slab_energy(adsorbate=None, site=None):
    s = fcc111("Cu", size=(3, 3, 4), a=a0, vacuum=8.0)
    s.set_constraint(FixAtoms(indices=[at.index for at in s if at.tag > 2]))   # tag 1 = top layer
    if adsorbate:
        add_adsorbate(s, adsorbate, 2.2, site)
    s.calc = EMT()
    BFGS(s, logfile=None).run(fmax=0.02)
    return s, s.get_potential_energy()

clean, e_clean = slab_energy()
from ase import Atoms
atom = Atoms("Au", positions=[[0, 0, 0]], cell=[10, 10, 10], pbc=True); atom.calc = EMT()
e_atom = atom.get_potential_energy()
res = {}
for site in ["ontop", "bridge", "fcc", "hcp"]:
    s, e = slab_energy("Au", site)
    res[site] = e - e_clean - e_atom
    write(f"Au_{site}.traj", s)
    print(f"Au/{site:7s}: E_ads = {res[site]:.3f} eV")
best = min(res, key=res.get); print("Most stable site:", best)
write("best_site.png", read(f"Au_{best}.traj"), rotation="-70x,-20y")
plt.bar(res.keys(), res.values()); plt.ylabel("E_ads (eV)"); plt.title("Au on Cu(111) (EMT)"); plt.savefig("adsorption.png", dpi=200)
