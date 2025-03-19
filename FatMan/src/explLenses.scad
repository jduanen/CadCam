// Generate STL for explosive lenses used in the Gadget

include <BOSL2/std.scad>
include <BOSL2/polyhedra.scad>

include <slowExpl.scad>


PENTA_COLOR = "red";
HEXA_COLOR = "blue";

PENT_SLOW_COLOR = "cyan";
HEX_SLOW_COLOR = "magenta";

LARGEST_RADIUS = 1500;
LARGEST_DIAMETER = (LARGEST_RADIUS * 2);

LENS_OUTER_RADIUS = 690.5625;  // from spreadsheet
LENS_OUTER_DIAMETER = (LENS_OUTER_RADIUS * 2);  // 1381.13
LENS_HEIGHT = 228.60;  // from spreadsheet
LENS_INNER_RADIUS = (LENS_OUTER_RADIUS - LENS_HEIGHT);  // 461.96
LENS_INNER_DIAMETER = (LENS_INNER_RADIUS * 2);  // 923.92

BOOSTER_OUTER_RADIUS = 461.16875;  // from spreadsheet
BOOSTER_OUTER_DIAMETER = (BOOSTER_OUTER_RADIUS * 2);  // 922.34
BOOSTER_HEIGHT = 225.425;  // from spreadsheet
BOOSTER_INNER_RADIUS = (BOOSTER_OUTER_RADIUS - BOOSTER_HEIGHT);
BOOSTER_INNER_DIAMETER = (BOOSTER_INNER_RADIUS * 2);

INTER_LENS_GAP = 0.025;

VERTICES = regular_polyhedron_info("vertices",
                                   d=LARGEST_DIAMETER,
                                   name="truncated icosahedron");
FACES = regular_polyhedron_info("faces",
                                d=LARGEST_DIAMETER,
                                name="truncated icosahedron");
NORMALS = regular_polyhedron_info("face normals",
                                  d=LARGEST_DIAMETER,
                                  name="truncated icosahedron");
assert(len(FACES) == len(NORMALS));

HEX_PYRAMID = 30;   // vertical hexagonal pyramid
PENT_PYRAMID = 29;  // pentagonal pyramid, rotated CCW on Y-axis

ALPHA = 0.5;

//-----------------------------------------------------------------------------
// make a max-sized hex/pent pyramid

module pentMaxPyramid(points, prismColor) {
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

module hexMaxPyramid(points, prismColor) {
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

module makeMaxPyramid(faceNum) {
        face = FACES[faceNum];
        normal = NORMALS[faceNum];
        if (len(face) == 5) {
            translate([for (n = normal) n * INTER_LENS_GAP])
                pentMaxPyramid(concat([for (f = face) VERTICES[f]], [[0,0,0]]), PENTA_COLOR);
        }
        if (len(face) == 6) {
            translate([for (n = normal) n * INTER_LENS_GAP])
                hexMaxPyramid(concat([for (f = face) VERTICES[f]], [[0,0,0]]), HEXA_COLOR);
        }
}

//-----------------------------------------------------------------------------
// make fast-only/full lenses and boosters

module truncatedIcosahedron() {
    for (i = [0:(len(FACES) - 1)]) {
        makeMaxPyramid(i);
    }
}

module lenses() {
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

module makeCombined() {
    union() {
        lenses();
        boosters();
    }
}

module combinedView() {
    difference() {
        makeCombined();
        viewSplitter();
    }
}

//-----------------------------------------------------------------------------
// make a representative hex/pent slow lens component

module hexSlowLens() {
    difference() {
        intersection() {
            makeMaxPyramid(HEX_PYRAMID);
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
                makeMaxPyramid(PENT_PYRAMID);
            color(PENT_SLOW_COLOR, 0.75)
                rotate_extrude()
                    polygon(points=pentPts);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

//-----------------------------------------------------------------------------
// make hex/slow compound lens (i.e., fast and slow components)
//// FIXME doesn't work
module compoundLens(pyramidNum) {
    face = FACES[pyramidNum];
    if (len(face) == 5) {
        compoundPentLens(pyramidNum);
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
            makeMaxPyramid(pyramidNum);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

module compoundPentLens(pyramidNum) {
    echo("TBD");
}

//-----------------------------------------------------------------------------
// make a given compound lens (includes fast and slow components)
//// FIXME doesn't work

module pentSlowLens(pyramidNum) {
    normal = NORMALS[pyramidNum];
    rotX = atan2(-normal.y, normal.z);
    rotY = atan2(normal.x, sqrt(normal.y * normal.y + normal.z * normal.z));
    difference() {
        difference() {
            rotate([rotX, rotY, 0])
                rotate_extrude()
                    polygon(points=pentPts);
            makeMaxPyramid(pyramidNum);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

module hexSlowLens(pyramidNum) {
    echo("TBD");
}

//-----------------------------------------------------------------------------
// make a given compound lens
//// FIXME only works for hex, need to add in pent case

module explLens(pyramidNum) {
    difference() {
        intersection() {
            union() {
                difference() {
                    normal = NORMALS[pyramidNum];
                    rotX = atan2(normal.y, normal.z);
                    rotY = atan2(-normal.x, sqrt(normal.y * normal.y + normal.z * normal.z));
                    rotate([rotX, rotY, 0])
                        makeMaxPyramid(pyramidNum);
                    translate([for (n = normal) n * INTER_LENS_GAP])
                        hexSlowLens();
                }
                hexSlowLens();
            }
            sphere(d=LENS_OUTER_DIAMETER);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

//-----------------------------------------------------------------------------
// make representative versions of each type of lens

module makeHexFastLensComponent() {
    difference() {
        makeHexFullFastLens();
        translate([0, 0, 0.01])  // space between components
            makeHexSlowLens();
        translate([0, 0, -0.01])  // space between components
            makeHexSlowLens();
    }
}

module makeHexFullFastLens() {  // no slow lens component
    face = FACES[HEX_PYRAMID];
    assert(len(face) == 6);
    normal = NORMALS[HEX_PYRAMID];
    rotX = atan2(normal.y, normal.z);
    rotY = atan2(-normal.x, sqrt(normal.y * normal.y + normal.z * normal.z));
    difference() {
        intersection() {
            rotate([rotX, rotY, 0])
                hexMaxPyramid(concat([for (f = face) VERTICES[f]], [[0,0,0]]), HEXA_COLOR);
            sphere(d=LENS_OUTER_DIAMETER);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

module makeHexSlowLens() {
    difference() {
        intersection() {
            makeMaxPyramid(HEX_PYRAMID);
            color("magenta", 0.75)
                rotate_extrude()
                    polygon(points=hexPts);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

module makeHexBooster(pyramidNum) {
    face = FACES[pyramidNum];
    assert(len(face) == 6);
    normal = NORMALS[HEX_PYRAMID];
    difference() {
        intersection() {
            translate([for (n = normal) n * INTER_LENS_GAP])
                hexMaxPyramid(concat([for (f = face) VERTICES[f]], [[0,0,0]]), HEXA_COLOR);
            sphere(d=BOOSTER_OUTER_DIAMETER);
        }
        sphere(d=BOOSTER_INNER_DIAMETER);
    }
}

module makePentFastLens() {  // void for slow lens
    difference() {
        makePentFullFastLens();
        translate([0, 0, 0.01])  // space between lenses
            makePentSlowLens();
        translate([0, 0, -0.01])  // space between lenses
            makePentSlowLens();
    }
}

module makePentFullFastLens() {  // no slow lens component
    face = FACES[PENT_PYRAMID];
    assert(len(face) == 5);
    normal = NORMALS[PENT_PYRAMID];
    rotX = atan2(normal.y, normal.z);
    rotY = atan2(-normal.x, sqrt(normal.y * normal.y + normal.z * normal.z));
    difference() {
        intersection() {
            rotate([rotX, rotY, 0])
                pentMaxPyramid(concat([for (f = face) VERTICES[f]], [[0,0,0]]), PENTA_COLOR);
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
                makeMaxPyramid(PENT_PYRAMID);
            color("cyan", 0.75)
                rotate_extrude()
                    polygon(points=pentPts);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

module makePentBooster(pyramidNum) {
    face = FACES[pyramidNum];
    assert(len(face) == 5);
    normal = NORMALS[PENT_PYRAMID];
    difference() {
        intersection() {
            translate([for (n = normal) n * INTER_LENS_GAP])
                pentMaxPyramid(concat([for (f = face) VERTICES[f]], [[0,0,0]]), PENTA_COLOR);
            sphere(d=BOOSTER_OUTER_DIAMETER);
        }
        sphere(d=BOOSTER_INNER_DIAMETER);
    }
}

//-----------------------------------------------------------------------------
// make complete sets of explosives

function hexPyramidNums() = [for (i = [0:len(FACES)-1]) if (len(FACES[i]) == 6) i];
function pentPyramidNums() = [for (i = [0:len(FACES)-1]) if (len(FACES[i]) == 5) i];

module makeHexBoosters() {
    for (n = hexPyramidNums()) {
        makeHexBooster(n);
    }
}

module makePentBoosters() {
    for (n = pentPyramidNums()) {
        makePentBooster(n);
    }
}

module makeBoosters() {
    makeHexBoosters();
    makePentBoosters();
}

module makeLenses() {
    makeHexSlowLens();
    makeHexFastLens();

    makePentSlowLens();
    makePentFastLens();
}

module makeAllExpls() {
    makeBoosters();
    makeLenses();
}

//-----------------------------------------------------------------------------
// the ones used in Fusion360

module boosts() {
    intersection() {
        difference() {
            truncatedIcosahedron();
            sphere(d=BOOSTER_INNER_DIAMETER);
        }
        sphere(d=BOOSTER_OUTER_DIAMETER);
    }
}

module lensesX() {
    intersection() {
        difference() {
            truncatedIcosahedron();
            sphere(d=LENS_INNER_DIAMETER);
        }
        sphere(d=LENS_OUTER_DIAMETER);
    }
}

module lenses() {
    difference() {
        intersection() {
            truncatedIcosahedron();
            sphere(d=LENS_OUTER_DIAMETER);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

//-----------------------------------------------------------------------------
//// TMP TMP TMP

module foo() {
    normal = NORMALS[PENT_PYRAMID];
    rotX = atan2(normal.y, normal.z);
    rotY = atan2(-normal.x, sqrt(normal.y * normal.y + normal.z * normal.z));
    rotate([rotX, rotY, 0])
        makeMaxPyramid(PENT_PYRAMID);
    translate([for (n = normal) n * INTER_LENS_GAP])
        pentSlowLens();
}

//num=12;
//for (i = [0:(num-1)]) makeMaxPyramid(i);

//=============================================================================

//$fn=128; //     20s HEX_BOOSTER
//$fn=512; //   4m20s HEX_BOOSTER
//$fn=1024; // 15m40s HEX_BOOSTER
//$fn = 1024;

HEX_BOOSTER = 0;
HEX_SLOW_LENS = 1;
HEX_FAST_LENS = 2;
PENT_BOOSTER = 3;
PENT_SLOW_LENS = 4;
PENT_FAST_LENS = 5;
HEX_LENS = 6;   // full fast lens
PENT_LENS = 7;  // full fast lens
BOOSTERS = 8;
LENSES = 9;
ALL = 10;

module makeGeometry(p) {
    if (p == HEX_BOOSTER) makeHexBooster(HEX_PYRAMID);
    else if (p == HEX_SLOW_LENS) makeHexSlowLens();
    else if (p == HEX_FAST_LENS) makeHexFastLens();
    else if (p == PENT_BOOSTER) makePentBooster(PENT_PYRAMID);
    else if (p == PENT_SLOW_LENS) makePentSlowLens();
    else if (p == PENT_FAST_LENS) makePentFastLens();
    else if (p == HEX_LENS) makeHexFullFastLens();
    else if (p == PENT_LENS) makePentFullFastLens();
    else if (p == BOOSTERS) makeBoosters();
    else if (p == LENSES) makeLenses();
    else if (p == ALL) makeAllExpls();
    else echo("Invalid pyramid selector: ", p);
}

//difference() {
//    //makeGeometry(PENT);
//    union() {
//        lensesX();
//        sphere(d=LENS_INNER_DIAMETER);
//        sphere(d=LENS_OUTER_DIAMETER);
//    }
//    viewSplitter();
//}

//makeGeometry(BOOSTERS);

//for (i = [0:7]) {
//    if (i < len(hexs)) makeHexBooster(hexs[i]);
//    if (i < len(pents)) makePentBooster(pents[i]);
//}

//INTER_LENS_GAP=1;

lenses();
