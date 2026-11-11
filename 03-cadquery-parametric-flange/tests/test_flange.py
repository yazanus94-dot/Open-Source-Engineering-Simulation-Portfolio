import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import pytest
from flange import make_flange


def test_volume_matches_analytic():
    od, t, hd, hh, bore, n, bd = 150, 18, 80, 25, 50, 6, 14
    part = make_flange(od, t, hd, hh, bore, n, 110, bd, fillet=0)
    expected = (math.pi * (od/2)**2 * t + math.pi * (hd/2)**2 * hh
                - math.pi * (bore/2)**2 * (t + hh) - n * math.pi * (bd/2)**2 * t)
    assert part.val().Volume() == pytest.approx(expected, rel=1e-3)


def test_invalid_bolt_circle():
    with pytest.raises(ValueError):
        make_flange(od=100, pcd=95, bolt_d=14)
