from pymatgen.core import Structure, Lattice
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer


def test_si_spacegroup():
    s = Structure.from_spacegroup("Fd-3m", Lattice.cubic(5.431), ["Si"], [[0, 0, 0]])
    assert SpacegroupAnalyzer(s).get_space_group_number() == 227
    assert len(s) == 8


def test_nacl_density():
    s = Structure.from_spacegroup("Fm-3m", Lattice.cubic(5.64), ["Na", "Cl"], [[0, 0, 0], [.5, .5, .5]])
    assert abs(s.density - 2.16) < 0.05
