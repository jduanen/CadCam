include <BOSL2/std.scad>
include <BOSL2/polyhedra.scad>

DIAMETER = 3000;
RADIUS = DIAMETER / 2;
GAP = 1.5;

vertices = regular_polyhedron_info("vertices", d=DIAMETER, name="truncated icosahedron");
faces = regular_polyhedron_info("faces", d=DIAMETER, name="truncated icosahedron");
normals = regular_polyhedron_info("face normals", d=DIAMETER, name="truncated icosahedron");

module pentagonalPyramid(points) {
   faces = [
        [0, 1, 2, 3, 4],  // base
        [5, 1, 0],        // side faces
        [5, 2, 1],
        [5, 3, 2],
        [5, 4, 3],
        [5, 0, 4]
    ];
    polyhedron(points = points, faces = faces, convexity = 5);
}

module hexagonalPyramid(points) {
    faces = [
        [0, 1, 2, 3, 4, 5],  // base
        [6, 1, 0],           // side faces
        [6, 2, 1],
        [6, 3, 2],
        [6, 4, 3],
        [6, 5, 4],
        [6, 0, 5]
    ];
    polyhedron(points = points, faces = faces, convexity = 6);
}

module truncatedIcosahedron(faces, vertices, normals, gap) {
    assert(len(faces) == len(normals));
    for (i = [0:32]) { //len(faces)-1]) {
        face = faces[i];
        echo(str("F: "), i, str(", "), face);
        normal = normals[i];
        echo(len(face));
        if (len(face) == 5) {
            translate([for (n = normal) n*gap])
                pentagonalPyramid(concat([for (f = face) vertices[f]], [[0,0,0]]));
        }
        if (len(face) == 6) {
            translate([for (n = normal) n*gap])
                hexagonalPyramid(concat([for (f = face) vertices[f]], [[0,0,0]]));
        }
    }
}

difference() {
    truncatedIcosahedron(faces, vertices, normals, GAP);
    //translate([0, -RADIUS, -RADIUS]) cube([RADIUS, DIAMETER, DIAMETER]);
}

