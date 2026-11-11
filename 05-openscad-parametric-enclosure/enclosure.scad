// Parametric electronics enclosure with screw posts, vents and snap lid
// Usage: openscad -o box.stl -D 'part="box"' enclosure.scad
part = "both";            // "box" | "lid" | "both"
pcb_l = 70; pcb_w = 50;   // PCB size [mm]
wall = 2; clearance = 0.4;
inner_h = 22;
post_d = 6; screw_d = 2.5; hole_off = 4;
vent_n = 6; vent_w = 1.6; vent_l = 20;
$fn = 48;

in_l = pcb_l + 2*clearance; in_w = pcb_w + 2*clearance;
out_l = in_l + 2*wall;      out_w = in_w + 2*wall;

module rounded_box(l, w, h, r) {
    hull() for (x=[r, l-r], y=[r, w-r]) translate([x, y, 0]) cylinder(r=r, h=h);
}

module posts() {
    for (x=[hole_off, pcb_l-hole_off], y=[hole_off, pcb_w-hole_off])
        translate([wall+clearance+x, wall+clearance+y, wall])
            difference() { cylinder(d=post_d, h=5); cylinder(d=screw_d, h=6); }
}

module box() {
    difference() {
        rounded_box(out_l, out_w, inner_h + wall, 3);
        translate([wall, wall, wall]) rounded_box(in_l, in_w, inner_h + 1, 1.5);
        // side vents
        for (i=[0:vent_n-1])
            translate([out_l/2 - vent_l/2, -1, wall + 6 + i*(vent_w+2.2)]) cube([vent_l, wall+2, vent_w]);
        // USB cut-out
        translate([out_l-wall-1, out_w/2-6, wall+5]) cube([wall+2, 12, 7]);
    }
    posts();
}

module lid() {
    rounded_box(out_l, out_w, wall, 3);
    translate([wall+clearance, wall+clearance, wall])
        difference() {
            rounded_box(in_l-2*clearance, in_w-2*clearance, 3, 1.5);
            translate([wall, wall, -1]) rounded_box(in_l-2*clearance-2*wall, in_w-2*clearance-2*wall, 5, 1);
        }
}

if (part == "box" || part == "both") box();
if (part == "lid" || part == "both") translate([0, out_w + 10, 0]) lid();
