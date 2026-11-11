"""Parametric pipe flange (CadQuery). Exports STEP + STL and prints mass properties."""
import argparse
import cadquery as cq

STEEL_DENSITY = 7850.0  # kg/m3


def make_flange(od=150.0, thickness=18.0, hub_d=80.0, hub_h=25.0,
                bore_d=50.0, bolt_n=6, pcd=110.0, bolt_d=14.0, fillet=0.0):
    """All dimensions in mm."""
    if bolt_d >= (od - pcd):
        raise ValueError("bolt holes break out of the flange edge")
    base = (cq.Workplane("XY").circle(od / 2).extrude(thickness)
            .faces(">Z").workplane()
            .polarArray(pcd / 2, 0, 360, bolt_n).hole(bolt_d))
    hub = cq.Workplane("XY").workplane(offset=thickness).circle(hub_d / 2).extrude(hub_h)
    body = base.union(hub).faces(">Z").workplane().hole(bore_d)
    return body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--od", type=float, default=150.0)
    ap.add_argument("--bolts", type=int, default=6)
    ap.add_argument("--out", default="flange")
    a = ap.parse_args()
    part = make_flange(od=a.od, bolt_n=a.bolts)
    vol_mm3 = part.val().Volume()
    print(f"Volume: {vol_mm3/1e3:.1f} cm3   Mass (steel): {vol_mm3*1e-9*STEEL_DENSITY:.3f} kg")
    cq.exporters.export(part, f"{a.out}.step")
    cq.exporters.export(part, f"{a.out}.stl")
    print("Wrote", a.out + ".step /", a.out + ".stl")


if __name__ == "__main__":
    main()
