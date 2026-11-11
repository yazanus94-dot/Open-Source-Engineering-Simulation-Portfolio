// 2D plate with a circular hole, meshed with Gmsh for Elmer
SetFactory("OpenCASCADE");
Rectangle(1) = {0, 0, 0, 0.2, 0.1};
Disk(2) = {0.1, 0.05, 0, 0.02};
BooleanDifference(3) = { Surface{1}; Delete; }{ Surface{2}; Delete; };
Mesh.CharacteristicLengthMax = 0.004;
Mesh.MshFileVersion = 2.2;
Physical Surface("plate", 1) = {3};
Physical Curve("hot_left", 2)  = {7};
Physical Curve("cold_right", 3) = {8};
Physical Curve("hole", 4) = {9};
