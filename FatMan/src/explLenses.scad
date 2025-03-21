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
                                   facedown=5,
                                   d=LARGEST_DIAMETER,
                                   name="truncated icosahedron");
FACES = regular_polyhedron_info("faces",
                                facedown=5,
                                d=LARGEST_DIAMETER,
                                name="truncated icosahedron");
NORMALS = regular_polyhedron_info("face normals",
                                  facedown=5,
                                  d=LARGEST_DIAMETER,
                                  name="truncated icosahedron");
assert(len(FACES) == len(NORMALS));

HEX_PYRAMID = 30;   // vertical hexagonal pyramid
PENT_PYRAMID = 29;  // pentagonal pyramid, rotated CCW on Y-axis

ALPHA = 0.5;

function isNan(x) = x != x;
function isEqual(a, b, eps=EPSILON) = abs(a - b) < eps;

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

module lensesX() {  // freecad doesn't like this one
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

module pentSlowLenses() {
    pentNums = pentPyramidNums();
    for (p = pentNums) {
        slowPentLens(p);
    }
}

module hexSlowLenses() {
    hexNums = hexPyramidNums();
    for (h = hexNums) {
        slowHexLens(h);
    }
}

module slowLenses() {
    pentSlowLenses();
    hexSlowLenses();
}

module slowPentLens(pyramidNum) {
    normal = NORMALS[pyramidNum];
    echo("Pent normal: ", normal);

    angle = acos(normal.z);
    // cross product of [0, 0, 1] and the normal
    axis = (isEqual(normal.x, 0) && isEqual(normal.y, 0)) ? [1, 0, 0] : [-normal.y, normal.x, 0];
    echo("angle: ", angle, ", axis: ", axis);
    difference() {
        intersection() {
            rotate(a=angle, v=axis)
                color(PENT_SLOW_COLOR, 0.75)
                    rotate_extrude()
                        polygon(points=pentPts);
            makeMaxPyramid(pyramidNum);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

module slowHexLens(pyramidNum) {
    n = NORMALS[pyramidNum];
    echo("Hex normal:", n);

    normal = [(isEqual(n.x, 0)) ? 0 :
              (isEqual(n.x, 1)) ? 1 :
              (isEqual(n.x, -1)) ? -1 :
              n.x,
              (isEqual(n.y, 0)) ? 0 :
              (isEqual(n.y, 1)) ? 1 :
              (isEqual(n.y, -1)) ? -1 :
              n.y,
              (isEqual(n.z, 0)) ? 0 :
              (isEqual(n.z, 1)) ? 1 :
              (isEqual(n.z, -1)) ? -1 :
              n.z];
    echo("Normal:", normal);
    angle = acos(normal.z);
    axis = [-normal.y, normal.x, 0];
    echo("angle:", angle, "axis:", axis);
    difference() {
        intersection() {
            rotate(a=angle, v=axis)
                color(HEX_SLOW_COLOR, 0.75)
                    rotate_extrude()
                        polygon(points=hexPts);
            makeMaxPyramid(pyramidNum);
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

//function isEq(a, b, eps=EPSILON) = abs(a - b) < eps;

module printNormals(F = 800) {
    for (n = NORMALS) {
        normal = [(isEqual(n.x, 0)) ? 0 :
                  (isEqual(n.x, 1)) ? 1 :
                  (isEqual(n.x, -1)) ? -1 :
                  n.x,
                  (isEqual(n.y, 0)) ? 0 :
                  (isEqual(n.y, 1)) ? 1 :
                  (isEqual(n.y, -1)) ? -1 :
                  n.y,
                  (isEqual(n.z, 0)) ? 0 :
                  (isEqual(n.z, 1)) ? 1 :
                  (isEqual(n.z, -1)) ? -1 :
                  n.z];
//      if (n != normal) echo(n, normal);
        pt = [normal[0] * F, normal[1] * F, normal[2] * F];
        echo(pt);
    }
}

module printAzEl() {
    for (n = NORMALS) {
        normal = [(isEqual(n.x, 0)) ? 0 :
                  (isEqual(n.x, 1)) ? 1 :
                  (isEqual(n.x, -1)) ? -1 :
                  n.x,
                  (isEqual(n.y, 0)) ? 0 :
                  (isEqual(n.y, 1)) ? 1 :
                  (isEqual(n.y, -1)) ? -1 :
                  n.y,
                  (isEqual(n.z, 0)) ? 0 :
                  (isEqual(n.z, 1)) ? 1 :
                  (isEqual(n.z, -1)) ? -1 :
                  n.z];
        az = acos(normal.z);
        el = atan2(normal.y, normal.x);
        if (el < 0) {
            el = el + 360;
        }
        echo(az, el);  // aka (phi, theta)
    }
}

module printTypeAzEl() {
    for (i = [0:len(NORMALS)-1]) {
        n = NORMALS[i];
        normal = [(isEqual(n.x, 0)) ? 0 :
                  (isEqual(n.x, 1)) ? 1 :
                  (isEqual(n.x, -1)) ? -1 :
                  n.x,
                  (isEqual(n.y, 0)) ? 0 :
                  (isEqual(n.y, 1)) ? 1 :
                  (isEqual(n.y, -1)) ? -1 :
                  n.y,
                  (isEqual(n.z, 0)) ? 0 :
                  (isEqual(n.z, 1)) ? 1 :
                  (isEqual(n.z, -1)) ? -1 :
                  n.z];
        az = acos(normal.z);
        el = atan2(normal.y, normal.x);
        if (el < 0) {
            el = el + 360;
        }
        typ = (len(FACES[i]) == 5) ? "  // Pentagon" : "  // Hexagon";
        echo(az, el, typ);  // aka (phi, theta) // <type>
    }
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

PENT_SLOW_LENSES = 10;
HEX_SLOW_LENSES = 11;

ALL = 12;

module makeGeometry(p) {
    if (p == HEX_BOOSTER) makeHexBooster(HEX_PYRAMID);
    else if (p == HEX_SLOW_LENS) makeHexSlowLens();
    else if (p == HEX_FAST_LENS) makeHexFastLens();

    else if (p == PENT_BOOSTER) makePentBooster(PENT_PYRAMID);
    else if (p == PENT_SLOW_LENS) makePentSlowLens();
    else if (p == PENT_FAST_LENS) makeFastLens();

    else if (p == HEX_LENS) makeHexFullFastLens();
    else if (p == PENT_LENS) makePentFullFastLens();

    else if (p == BOOSTERS) boosters();
    else if (p == LENSES) lenses();

    else if (p == HEX_SLOW_LENSES) hexSlowLenses();
    else if (p == PENT_SLOW_LENSES) pentSlowLenses();

    else if (p == ALL) makeAllExpls();
    else echo("Invalid pyramid selector: ", p);
}

//difference() {
//    slowPentLens(PENT_PYRAMID);
//    makeGeometry(HEX_SLOW_LENS);
    //viewSplitter();
//}

//pNums = pentPyramidNums();
//hNums = hexPyramidNums();
//num = 1;
//for (i = [0:(num-1)]) {
//    echo("Pyramid #: ", hNums[i]);
//    slowHexLens(hNums[i]);
//    color("gray", 0.5)
//    makeMaxPyramid(hNums[i]);
//}

makeGeometry(PENT_SLOW_LENSES);  // works
//makeGeometry(HEX_SLOW_LENSES);  // doesn't work

//hexNums = hexPyramidNums();
//echo(hexNums);
//for (i = [1:19]) {
//    h = hexNums[i];
//    echo("HEX#", h);
//    slowHexLens(h);
//}

//regular_polyhedron("truncated icosahedron", facedown=5, d=LENS_OUTER_DIAMETER);
