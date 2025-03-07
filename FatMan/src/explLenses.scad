// Generate STL for explosive lenses used in the Gadget

include <BOSL2/std.scad>
include <BOSL2/polyhedra.scad>

include <slowExpl.scad>


PENTA_COLOR = "red";
HEXA_COLOR = "blue";

PENT_SLOW_COLOR = "cyan";
HEX_SLOW_COLOR = "magenta";

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

GAP = INTER_LENS_GAP;
VERTICES = regular_polyhedron_info("vertices", d=LARGEST_DIAMETER, name="truncated icosahedron");
FACES = regular_polyhedron_info("faces", d=LARGEST_DIAMETER, name="truncated icosahedron");
NORMALS = regular_polyhedron_info("face normals", d=LARGEST_DIAMETER, name="truncated icosahedron");

HEX_PYRAMID = 30;   // vertical hexagonal pyramid
PENT_PYRAMID = 29;  // pentagonal pyramid, rotated CCW on Y-axis

ALPHA = 0.5;

module pentagonalPyramid(points, prismColor) {
   faceIndices = [
        [0, 1, 2, 3, 4],  // base
        [5, 1, 0],        // side faces
        [5, 2, 1],
        [5, 3, 2],
        [5, 4, 3],
        [5, 0, 4]
    ];
    color(prismColor, ALPHA)
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
    color(prismColor, ALPHA)
        polyhedron(points = points, faces = faceIndices, convexity = 6);
}

module makePyramid(faceNum) {
        face = FACES[faceNum];
        normal = NORMALS[faceNum];
        if (len(face) == 5) {
            translate([for (n = normal) n * GAP])
                pentagonalPyramid(concat([for (f = face) VERTICES[f]], [[0,0,0]]), PENTA_COLOR);
        }
        if (len(face) == 6) {
            translate([for (n = normal) n * GAP])
                hexagonalPyramid(concat([for (f = face) VERTICES[f]], [[0,0,0]]), HEXA_COLOR);
        }
}

//----------------------------------------------

module truncatedIcosahedron() {
    assert(len(FACES) == len(NORMALS));
    for (i = [0:(len(FACES) - 1)]) {
        makePyramid(i);
    }
}

module explosiveLenses() {
    difference() {
        intersection() {
            truncatedIcosahedron();
            sphere(d=LENS_OUTER_DIAMETER);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

module boosters() {
    difference() {
        intersection() {
            truncatedIcosahedron();
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

//----------------------------------------------

module hexSlowLens() {
    difference() {
        intersection() {
            makePyramid(HEX_PYRAMID);
            color(HEX_SLOW_COLOR, 0.75)
                rotate_extrude()
                    polygon(points=hexPts);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

module pentSlowLens() {
    normal = NORMALS[PENT_PYRAMID];
    rotX = atan2(normal.y, normal.z);
    rotY = atan2(-normal.x, sqrt(normal.y * normal.y + normal.z * normal.z));
    difference() {
        intersection() {
            rotate([rotX, rotY, 0])
                makePyramid(PENT_PYRAMID);
            color(PENT_SLOW_COLOR, 0.75)
                rotate_extrude()
                    polygon(points=pentPts);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

module compoundLens(pyramidNum) {
    face = FACES[pyramidNum];
    if (len(face) == 5) {
        compoundHexLens(pyramidNum);
    }
    if (len(face) == 6) {
        compoundHexLens(pyramidNum);
    }
}

module compoundHexLens(pyramidNum) {
    normal = NORMALS[pyramidNum];
    rotX = atan2(-normal.y, normal.z);
    rotY = atan2(normal.x, sqrt(normal.y * normal.y + normal.z * normal.z));
    difference() {
        difference() {
            rotate([rotX, rotY, 0])
                rotate_extrude()
                    polygon(points=hexPts);
            makePyramid(pyramidNum);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

module pentSlowLens(pyramidNum) {
    normal = NORMALS[pyramidNum];
    rotX = atan2(-normal.y, normal.z);
    rotY = atan2(normal.x, sqrt(normal.y * normal.y + normal.z * normal.z));
    difference() {
        difference() {
            rotate([rotX, rotY, 0])
                rotate_extrude()
                    polygon(points=pentPts);
            makePyramid(pyramidNum);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

module explLens(pyramidNum) {
    difference() {
        intersection() {
            union() {
                difference() {
                    normal = NORMALS[pyramidNum];
                    rotX = atan2(normal.y, normal.z);
                    rotY = atan2(-normal.x, sqrt(normal.y * normal.y + normal.z * normal.z));
                    rotate([rotX, rotY, 0])
                        makePyramid(pyramidNum);
                    translate([for (n = normal) n * GAP])
                        hexSlowLens();
                }
                hexSlowLens();
            }
            sphere(d=LENS_OUTER_DIAMETER);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

//---------------------------------

module makeHexFastLens() {
    difference() {
        makeHexFullFastLens();
        translate([0, 0, 0.01])  // space between lenses
            makeHexSlowLens();
        translate([0, 0, -0.01])  // space between lenses
            makeHexSlowLens();
    }
}

module makeHexFullFastLens() {
    face = FACES[HEX_PYRAMID];
    assert(len(face) == 6);
    normal = NORMALS[HEX_PYRAMID];
    rotX = atan2(normal.y, normal.z);
    rotY = atan2(-normal.x, sqrt(normal.y * normal.y + normal.z * normal.z));
    difference() {
        intersection() {
            rotate([rotX, rotY, 0])
                hexagonalPyramid(concat([for (f = face) VERTICES[f]], [[0,0,0]]), HEXA_COLOR);
            sphere(d=LENS_OUTER_DIAMETER);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

module makeHexSlowLens() {
    difference() {
        intersection() {
            makePyramid(HEX_PYRAMID);
            color("magenta", 0.75)
                rotate_extrude()
                    polygon(points=hexPts);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

module makeHexBooster() {
    face = FACES[HEX_PYRAMID];
    echo("HB: ", [for (f = face) VERTICES[f]]);
    assert(len(face) == 6);
    normal = NORMALS[HEX_PYRAMID];
    difference() {
        intersection() {
            hexagonalPyramid(concat([for (f = face) VERTICES[f]], [[0,0,0]]), HEXA_COLOR);
            sphere(d=BOOSTER_OUTER_DIAMETER);
        }
        sphere(d=BOOSTER_INNER_DIAMETER);
    }
}

module makePentFastLens() {
    difference() {
        makePentFullFastLens();
        translate([0, 0, 0.01])  // space between lenses
            makePentSlowLens();
        translate([0, 0, -0.01])  // space between lenses
            makePentSlowLens();
    }
}

module makePentFullFastLens() {
    face = FACES[PENT_PYRAMID];
    assert(len(face) == 5);
    normal = NORMALS[PENT_PYRAMID];
    rotX = atan2(normal.y, normal.z);
    rotY = atan2(-normal.x, sqrt(normal.y * normal.y + normal.z * normal.z));
    difference() {
        intersection() {
            rotate([rotX, rotY, 0])
                pentagonalPyramid(concat([for (f = face) VERTICES[f]], [[0,0,0]]), PENTA_COLOR);
            sphere(d=LENS_OUTER_DIAMETER);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

module makePentSlowLens() {
    normal = NORMALS[PENT_PYRAMID];
    rotX = atan2(normal.y, normal.z);
    rotY = atan2(-normal.x, sqrt(normal.y * normal.y + normal.z * normal.z));
    difference() {
        intersection() {
            rotate([rotX, rotY, 0])
                makePyramid(PENT_PYRAMID);
            color("cyan", 0.75)
                rotate_extrude()
                    polygon(points=pentPts);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

module makePentBooster() {
    face = FACES[PENT_PYRAMID];
    assert(len(face) == 5);
    normal = NORMALS[PENT_PYRAMID];
    rotX = atan2(normal.y, normal.z);
    rotY = atan2(-normal.x, sqrt(normal.y * normal.y + normal.z * normal.z));
    difference() {
        intersection() {
            rotate([rotX, rotY, 0])
                pentagonalPyramid(concat([for (f = face) VERTICES[f]], [[0,0,0]]), PENTA_COLOR);
            sphere(d=BOOSTER_OUTER_DIAMETER);
        }
        sphere(d=BOOSTER_INNER_DIAMETER);
    }
}

///////////////////////////

//num=12;
//for (i = [0:(num-1)]) makePyramid(i);

module foo() {
    normal = NORMALS[PENT_PYRAMID];
    rotX = atan2(normal.y, normal.z);
    rotY = atan2(-normal.x, sqrt(normal.y * normal.y + normal.z * normal.z));
    rotate([rotX, rotY, 0])
        makePyramid(PENT_PYRAMID);
    translate([for (n = normal) n * GAP])
        pentSlowLens();
}

module allLens() {
    makeHexBooster();
    makeHexSlowLens();
    makeHexFastLens();

    makePentBooster();
    makePentSlowLens();
    makePentFastLens();
}

//difference() {
//    allLens();
//    viewSplitter();
//}

//$fn=128; //     20s HEX_BOOSTER
//$fn=512; //   4m20s HEX_BOOSTER
//$fn=1024; // 15m40s HEX_BOOSTER
$fn = 1024;

HEX_BOOSTER = 0;
HEX_SLOW_LENS = 1;
HEX_FAST_LENS = 2;

PENT_BOOSTER = 3;
PENT_SLOW_LENS = 4;
PENT_FAST_LENS = 5;

HEX_LENS = 6;   // full fast lens
PENT_LENS = 7;  // full fast lens

p = PENT_LENS;

if (p == HEX_BOOSTER) makeHexBooster();
else if (p == HEX_SLOW_LENS) makeHexSlowLens();
else if (p == HEX_FAST_LENS) makeHexFastLens();
else if (p == PENT_BOOSTER) makePentBooster();
else if (p == PENT_SLOW_LENS) makePentSlowLens();
else if (p == PENT_FAST_LENS) makePentFastLens();
else if (p == HEX_LENS) makeHexFullFastLens();
else if (p == PENT_LENS) makePentFullFastLens();
else echo("Invalid pyramid selector: ", p);
