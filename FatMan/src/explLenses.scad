// Generate STL for explosive lenses used in the Gadget

include <BOSL2/std.scad>
include <BOSL2/polyhedra.scad>

PENTA_COLOR = "red";
HEXA_COLOR = "blue";

//// FIXME use actual dimensions
LARGEST_RADIUS = 1500;
LARGEST_DIAMETER = (LARGEST_RADIUS * 2);

LENS_OUTER_RADIUS = 688.975;
LENS_OUTER_DIAMETER = (LENS_OUTER_RADIUS * 2);  // 1377.95
LENS_HEIGHT = 224.425;
LENS_INNER_RADIUS = (LENS_OUTER_RADIUS - LENS_HEIGHT);  // 465.55
LENS_INNER_DIAMETER = (LENS_INNER_RADIUS * 2);
LENS_FELT_GAP = 2;

BOOSTER_OUTER_RADIUS = 463.55;
BOOSTER_OUTER_DIAMETER = (BOOSTER_OUTER_RADIUS * 2);  // 927.1
BOOSTER_HEIGHT = 228.6;
BOOSTER_INNER_RADIUS = (BOOSTER_OUTER_RADIUS - BOOSTER_HEIGHT);
BOOSTER_INNER_DIAMETER = (BOOSTER_INNER_RADIUS * 2);
BOOSTER_FELT_GAP = 2;

INTER_LENS_GAP = 0.5;

PUSHER_OUTER_RADIUS = 234.95;
PUSHER_OUTER_DIAMETER = (PUSHER_OUTER_RADIUS * 2);

gap = INTER_LENS_GAP;
vertices = regular_polyhedron_info("vertices", d=LARGEST_DIAMETER, name="truncated icosahedron");
faces = regular_polyhedron_info("faces", d=LARGEST_DIAMETER, name="truncated icosahedron");
normals = regular_polyhedron_info("face normals", d=LARGEST_DIAMETER, name="truncated icosahedron");

module pentagonalPyramid(points, prismColor) {
   faceIndices = [
        [0, 1, 2, 3, 4],  // base
        [5, 1, 0],        // side faces
        [5, 2, 1],
        [5, 3, 2],
        [5, 4, 3],
        [5, 0, 4]
    ];
    color(prismColor)
        polyhedron(points = points, faces = faceIndices, convexity = 5);
}

module hexagonalPyramid(points, prismColor) {
    faceIndices = [
        [0, 1, 2, 3, 4, 5],  // base
        [6, 1, 0],           // side faces
        [6, 2, 1],
        [6, 3, 2],
        [6, 4, 3],
        [6, 5, 4],
        [6, 0, 5]
    ];
    color(prismColor)
        polyhedron(points = points, faces = faceIndices, convexity = 6);
}

module makePyramid(faceNum) {
        face = faces[faceNum];
        normal = normals[faceNum];
        if (len(face) == 5) {
            translate([for (n = normal) n * gap])
                pentagonalPyramid(concat([for (f = face) vertices[f]], [[0,0,0]]), PENTA_COLOR);
        }
        if (len(face) == 6) {
            translate([for (n = normal) n * gap])
                hexagonalPyramid(concat([for (f = face) vertices[f]], [[0,0,0]]), HEXA_COLOR);
        }
}

module truncatedIcosahedron(faces, vertices, normals, gap) {
    assert(len(faces) == len(normals));
    for (i = [0:(len(faces) - 1)]) {
        makePyramid(i);
    }
}

module explosiveLenses() {
    difference() {
        intersection() {
            truncatedIcosahedron(faces, vertices, normals, INTER_LENS_GAP);
            sphere(d=LENS_OUTER_DIAMETER);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

module boosters() {
    difference() {
        intersection() {
            truncatedIcosahedron(faces, vertices, normals, INTER_LENS_GAP);
            sphere(d=BOOSTER_OUTER_DIAMETER);
        }
        sphere(d=BOOSTER_INNER_DIAMETER);
    }
}

module viewSplitter() {
    translate([0, -LARGEST_RADIUS, -LARGEST_RADIUS])
        cube([LARGEST_DIAMETER, LARGEST_DIAMETER, LARGEST_DIAMETER]);
}

module combined() {
    union() {
        explosiveLenses();
        boosters();
    }
}

module combinedView() {
    difference() {
        combined();
        viewSplitter();
    }
}

//$fn = 128;

//num=12;
//for (i = [0:(num-1)]) makePyramid(i);

//combined();
