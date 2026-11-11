all: box.stl lid.stl
box.stl: enclosure.scad
	openscad -o $@ -D 'part="box"' $<
lid.stl: enclosure.scad
	openscad -o $@ -D 'part="lid"' $<
preview.png: enclosure.scad
	openscad -o $@ --imgsize=1200,800 --autocenter --viewall $<
