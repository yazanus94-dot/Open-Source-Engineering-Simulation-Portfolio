# PCB layout & release checklist (Pcbnew)
1. `python netlist.py` -> `555_blinker.net`; Pcbnew: *File > Import > Netlist*.
2. Board 40 x 25 mm, 2 layers, 0.25 mm tracks (signal), 0.5 mm (power), 0.2 mm clearance (JLCPCB/PCBWay capable).
3. Place C3 within 5 mm of U1 pin 8/1; keep timing network (R1, R2, C1) compact and away from the LED current path.
4. Solid GND pour on both layers, stitch vias around the board edge.
5. Run **DRC** (zero errors) and **ERC** in the schematic editor.
6. Export: Gerbers + drill (`File > Plot`), BOM (`bom.csv`), pick-and-place, 3D view screenshot for the README.
7. Commit the `.kicad_pro/.kicad_sch/.kicad_pcb` files and screenshots to this folder.
