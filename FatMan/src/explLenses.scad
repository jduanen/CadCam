// Generate STL for explosive lenses used in the Gadget

include <BOSL2/std.scad>
include <BOSL2/polyhedra.scad>

include <scad/hexSlowLens.scad>
include <scad/pentSlowLens.scad>


PENTA_COLOR = "red";
HEXA_COLOR = "blue";

PENT_FAST_COLOR = "cyan";
HEX_FAST_COLOR = "magenta";

PENT_SLOW_COLOR = "green";
HEX_SLOW_COLOR = "yellow";

LARGEST_RADIUS = 1500;
LARGEST_DIAMETER = (LARGEST_RADIUS * 2);

//// FIXME use a common file derived from the spreadsheet
LENS_OUTER_RADIUS = 690.5625;
LENS_OUTER_DIAMETER = 1381.125;
LENS_INNER_RADIUS = 461.9625;
LENS_INNER_DIAMETER = 923.925;

BOOSTER_OUTER_RADIUS = 461.16875;
BOOSTER_OUTER_DIAMETER = 922.3375;
BOOSTER_INNER_RADIUS = 235.74375;
BOOSTER_INNER_DIAMETER = 471.4875;

INTER_LENS_GAP = 0.025;

// representative pyramid numbers
HEX_PYRAMID_NUM = 20;   // pentagonal pyramid, rotated CCW on Y-axis
PENT_PYRAMID_NUM = 28;  // vertical hexagonal pyramid

ALPHA = 0.5;

//-----------------------------------------------------------------------------
// Create truncated icosahedron data (pentagonal face up/down)

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

//-----------------------------------------------------------------------------
// Utility functions

function isNan(x) = x != x;
function isEqual(a, b, eps=EPSILON) = abs(a - b) < eps;

function hexPyramidNums() = [for (i = [0:len(FACES)-1]) if (len(FACES[i]) == 6) i];
function pentPyramidNums() = [for (i = [0:len(FACES)-1]) if (len(FACES[i]) == 5) i];

function quantizeNormal(norm) = [(isEqual(norm.x, 0)) ? 0 :
                                 (isEqual(norm.x, 1)) ? 1 :
                                 (isEqual(norm.x, -1)) ? -1 :
                                 norm.x,
                                 (isEqual(norm.y, 0)) ? 0 :
                                 (isEqual(norm.y, 1)) ? 1 :
                                 (isEqual(norm.y, -1)) ? -1 :
                                 norm.y,
                                 (isEqual(norm.z, 0)) ? 0 :
                                 (isEqual(norm.z, 1)) ? 1 :
                                 (isEqual(norm.z, -1)) ? -1 :
                                 norm.z];

//-----------------------------------------------------------------------------
// Tools for making cross-section views

module viewSplitter() {
    translate([0, -LARGEST_RADIUS, -LARGEST_RADIUS])
        cube([LARGEST_DIAMETER, LARGEST_DIAMETER, LARGEST_DIAMETER]);
}

module splitView() {
    difference() {
        children();
        viewSplitter();
    }
}

//-----------------------------------------------------------------------------
// Print truncated icosahedron info

module printNormals(F = 800) {
    for (n = NORMALS) {
        normal = quantizeNormal(n);
        pt = [normal[0] * F, normal[1] * F, normal[2] * F];
        echo(pt);
    }
}

module printAzEl() {
    for (n = NORMALS) {
        normal = quantizeNormal(n);
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
        normal = quantizeNormal(n);
        az = acos(normal.z);
        el = atan2(normal.y, normal.x);
        if (el < 0) {
            el = el + 360;
        }
        typ = (len(FACES[i]) == 5) ? "  // Pentagon" : "  // Hexagon";
        echo(az, el, typ);  // aka (phi, theta) // <type>
    }
}

//-----------------------------------------------------------------------------
// Make max-sized hex/pent pyramids for tools
//// XXX

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

module makeMaxPyramid(pyramidNum) {
        face = FACES[pyramidNum];
        normal = NORMALS[pyramidNum];
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
// Make the various types of lenses

//// XXX
module makeHexBooster(pyramidNum) {
    face = FACES[pyramidNum];
    assert(len(face) == 6);
    normal = NORMALS[pyramidNum];
    difference() {
        intersection() {
            translate([for (n = normal) n * INTER_LENS_GAP])
                hexMaxPyramid(concat([for (f = face) VERTICES[f]], [[0,0,0]]), HEXA_COLOR);
            sphere(d=BOOSTER_OUTER_DIAMETER);
        }
        sphere(d=BOOSTER_INNER_DIAMETER);
    }
}

//// XXX
module makePentBooster(pyramidNum) {
    face = FACES[pyramidNum];
    assert(len(face) == 5);
    normal = NORMALS[pyramidNum];
    difference() {
        intersection() {
            translate([for (n = normal) n * INTER_LENS_GAP])
                pentMaxPyramid(concat([for (f = face) VERTICES[f]], [[0,0,0]]), PENTA_COLOR);
            sphere(d=BOOSTER_OUTER_DIAMETER);
        }
        sphere(d=BOOSTER_INNER_DIAMETER);
    }
}


module baz() {  // makeslowlenscomponent
    normal = NORMALS[HEX_PYRAMID_NUM];
    angle = acos(normal.z);

    intersection () {
        rotate([0, -angle, 0])
            makeMaxPyramid(HEX_PYRAMID_NUM); // align to top
        color("magenta", 0.75)
            hexSlowLens();  // already aligned to top
    }
}

//// XXX
module makeHexFastLensComponent() { // no slow lens
    difference() {
        difference() {
            makeHexFastLensFull(HEX_PYRAMID_NUM);
            translate([0, 0, 0.01])  // leave space between components
                makeHexSlowLensComponent();
        }
    }
}

//// XXX
module makePentFastLensComponent() {  // no slow lens
    difference() {
        makePentFastLensFull(PENT_PYRAMID_NUM);
        translate([0, 0, 0.01])  // space between lenses
            makePentSlowLensComponent();
    }
}

//// XXX
module makeCompoundHexLens() { // both fast and slow lenses
    makeHexSlowLensComponent();
    makeHexFastLensComponent();
}

//// XXX
module makeCompoundPentLens() { // both fast and slow lenses
    makePentSlowLensComponent();
    makePentFastLensComponent();
}

//// XXX
module makeHexBoosters() {
    for (n = hexPyramidNums()) {
        makeHexBooster(n);
    }
}

//// XXX
module makePentBoosters() {
    for (n = pentPyramidNums()) {
        makePentBooster(n);
    }
}

//// XXX
module makeBoosters() {
    makeHexBoosters();
    makePentBoosters();
}

//// XXX
module makeHexSlowLens(pyramidNum) {
    assert(len(FACES[pyramidNum]) == 6);
    makeSlowLens(pyramidNum);
}

//// XXX
module makePentSlowLens(pyramidNum) {
    assert(len(FACES[pyramidNum]) == 5);
    makeSlowLens(pyramidNum);
}

//// XXX
module makeSlowLens(pyramidNum) {
    n = NORMALS[pyramidNum];
    normal = quantizeNormal(n);
    angle = acos(normal.z);
    axis = (normal == [0, 0, -1]) ? [1, 0, 0] : [-normal.y, normal.x, 0];
    f = len(FACES[pyramidNum]);
    c = (f == 6) ? HEX_SLOW_COLOR : PENT_SLOW_COLOR;
    difference() {
        intersection() {
            rotate(a=angle, v=axis)
                color(c, 0.75)
                    if (f == 6) hexSlowLens(); else pentSlowLens();
            makeMaxPyramid(pyramidNum);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

//// XXX
module makeHexSlowLensComponent() {
    normal = NORMALS[HEX_PYRAMID_NUM];
    angle = acos(normal.z);

    intersection () {
        rotate([0, -angle, 0])
            makeMaxPyramid(HEX_PYRAMID_NUM); // align to top
        color("magenta", 0.75)
            hexSlowLens();  // already aligned to top
    }
}

//// XXX
module makePentSlowLensComponent() {
    intersection () {
        makeMaxPyramid(PENT_PYRAMID_NUM);  // already aligned to top
        color("cyan", 0.75)
            pentSlowLens();  // already aligned to top
    }
}

//// ????
module makeHexFastLensFull(pyramidNum) {
    assert(len(FACES[pyramidNum]) == 6);
    makeFastLensFull(pyramidNum);
}

//// ????
module makePentFastLensFull(pyramidNum) {
    assert(len(FACES[pyramidNum]) == 5);
    makeFastLensFull(pyramidNum);
}

//// ????
module makeFastLensFull(pyramidNum) {  // full size of combined lens components, just one part
    n = NORMALS[pyramidNum];
    normal = quantizeNormal(n);
    angle = acos(normal.z);
    axis = (normal == [0, 0, -1]) ? [1, 0, 0] : [-normal.y, normal.x, 0];
    f = len(FACES[pyramidNum]);
    c = (f == 6) ? HEX_FAST_COLOR : PENT_FAST_COLOR;
    difference() {
        intersection() {
            color(c)
                makeMaxPyramid(pyramidNum);
            sphere(d=LENS_OUTER_DIAMETER);
        }
        sphere(d=LENS_INNER_DIAMETER);
    }
}

module XXXmakePentFastLensFull() {  // no slow lens component
    face = FACES[PENT_PYRAMID_NUM];
    assert(len(face) == 5);
    normal = NORMALS[PENT_PYRAMID_NUM];
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

module makeFastLens(pyramidNum) {
    n = NORMALS[pyramidNum];
    normal = quantizeNormal(n);
    angle = acos(normal.z);
    axis = (normal == [0, 0, -1]) ? [1, 0, 0] : [-normal.y, normal.x, 0];
    f = len(FACES[pyramidNum]);
    c = (f == 6) ? HEX_FAST_COLOR : PENT_FAST_COLOR;
    difference() {
        rotate(a=angle, v=axis)
            color(c, 0.75)
                if (f == 6) makeHexFastLensComponent(); else makePentFastLensComponent();
        makeMaxPyramid(pyramidNum);
        sphere(d=LENS_INNER_DIAMETER);
    }
}

//// XXX
module makeHexFastLens(pyramidNum) {
    assert(len(FACES[pyramidNum]) == 6);
    makeFastLens(pyramidNum);
}

//// XXX
module makePentFastLens(pyramidNum) {
    assert(len(FACES[pyramidNum]) == 5);
    makeFastLens(pyramidNum);
}


//// XXX
module makeHexFastLenses() {
    hexNums = hexPyramidNums();
    for (h = hexNums) {
        makeHexFastLens(h);
    }
}

//// XXX
module makePentFastLenses() {
    pentNums = pentPyramidNums();
    for (p = pentNums) {
        makePentFastLens(p);
    }
}

//// XXX
module makeHexSlowLenses() {
    hexNums = hexPyramidNums();
    for (h = hexNums) {
        makeHexSlowLens(h);
    }
}

//// XXX
module makePentSlowLenses() {
    pentNums = pentPyramidNums();
    for (p = pentNums) {
        makePentSlowLens(p);
    }
}

//// 
module makeFastLenses() {
    makeHexFastLenses();
    makePentFastenses();
}

//// XXX
module makeSlowLenses() {
    makeHexSlowLenses();
    makePentSlowLenses();
}

// XXX
module makeLenses() {
    makeHexSlowLensComponent();
    makeHexFastLensComponent();

    makePentSlowLensComponent();
    makePentFastLensComponent();
}

//-----------------------------------------------------------------------------
// alternative approaches to making prisms

module truncatedIcosahedron() {
    for (i = [0:(len(FACES) - 1)]) {
        makeMaxPyramid(i);
    }
}

module boosts() {
    intersection() {
        difference() {
            truncatedIcosahedron();
            sphere(d=BOOSTER_INNER_DIAMETER);
        }
        sphere(d=BOOSTER_OUTER_DIAMETER);
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

module lensesX() {  // freecad doesn't like this one
    intersection() {
        difference() {
            truncatedIcosahedron();
            sphere(d=LENS_INNER_DIAMETER);
        }
        sphere(d=LENS_OUTER_DIAMETER);
    }
}

module makeCombined() {
    union() {
        boosters();
        lenses();
    }
}

//-----------------------------------------------------------------------------
//// TMP TMP TMP

//num=12;
//for (i = [0:(num-1)]) makeMaxPyramid(i);

//regular_polyhedron("truncated icosahedron", facedown=5, d=LENS_OUTER_DIAMETER);

module foo() {
    normal = NORMALS[PENT_PYRAMID_NUM];
    rotX = atan2(normal.y, normal.z);
    rotY = atan2(-normal.x, sqrt(normal.y * normal.y + normal.z * normal.z));
    rotate([rotX, rotY, 0])
        makeMaxPyramid(PENT_PYRAMID_NUM);
    translate([for (n = normal) n * INTER_LENS_GAP])
        pentSlowLens();
}

//function isEq(a, b, eps=EPSILON) = abs(a - b) < eps;

//splitView() {
//    makeGeometry(BOOSTERS);
//    makeGeometry(LENSES);
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

//hexNums = hexPyramidNums();
//echo(hexNums);
//for (i = [1:19]) {
//    h = hexNums[i];
//    echo("HEX#", h);
//    slowHexLens(h);
//}

//=============================================================================

//$fn=128; //     20s HEX_BOOSTER
//$fn=512; //   4m20s HEX_BOOSTER
//$fn=1024; // 15m40s HEX_BOOSTER
//$fn = 1024;

HEX_BOOSTER = 0;        // representative hexagonal booster (vertical) //// XXX
PENT_BOOSTER = 1;       // representative pentagonal booster (vertical) //// XXX
HEX_FAST_LENS = 2;      // representative hexagonal fast lens (vertical)
PENT_FAST_LENS = 3;     // representative pentagonal fast lens (?)
HEX_SLOW_LENS = 4;      // representative hexagonal slow lens (vertical)
PENT_SLOW_LENS = 5;     // representative pentagonal slow lens (?)
HEX_LENS = 6;           // includes both fast and slow lens hexagonal components
PENT_LENS = 7;          // includes both fast and slow lens pentagonal components
HEX_LENS_EXT = 8;       // external of combined both lens hexagonal components
PENT_LENS_EXT = 9;      // external of combined both lens pentagonal components
HEX_SLOW_LENSES = 10;   // all hexagonal slow lens components
PENT_SLOW_LENSES = 11;  // all pentagonal slow lens components
BOOSTERS = 12;          // all boosters (hexagonal and pentagonal)
FAST_LENSES = 13;       // all fast lenses (hexagonal and pentagonal)
SLOW_LENSES = 14;       // all slow lenses (hexagonal and pentagonal)
LENSES = 15;            // all lenses (both fast and slow, hexagonal and pentagonal)


module makeGeometry(p) {
    if (p == HEX_BOOSTER) makeHexBooster(HEX_PYRAMID_NUM);
    else if (p == PENT_BOOSTER) makePentBooster(PENT_PYRAMID_NUM);

    else if (p == HEX_FAST_LENS) makeHexFastLensComponent();
    else if (p == PENT_FAST_LENS) makePentFastLensComponent();

    else if (p == HEX_SLOW_LENS) makeHexSlowLensComponent();
    else if (p == PENT_SLOW_LENS) makePentSlowLensComponent();

    else if (p == HEX_LENS) makeCompoundHexLens();
    else if (p == PENT_LENS) makeCompoundPentLens();

    else if (p == HEX_LENS_EXT) makeHexFastLensFull(HEX_PYRAMID_NUM);
    else if (p == PENT_LENS_EXT) makePentFastLensFull(PENT_PYRAMID_NUM);

    else if (p == BOOSTERS) makeBoosters();

    else if (p == HEX_SLOW_LENSES) makeHexSlowLenses();
    else if (p == PENT_SLOW_LENSES) makePentSlowLenses();

    else if (p == FAST_LENSES) makeFastLenses();
    else if (p == SLOW_LENSES) makeSlowLenses();

    else if (p == LENSES) makeLenses();

    else echo("Invalid pyramid selector: ", p);
}

//-----------------------------------------------------------------------------
// make a representative hex/pent slow lens component

//=============================================================================

//splitView() {
//    color("red", 0.75)
//        makePentFastLensFull();
//    makeGeometry(SLOW_LENSES);
//}

if (0) {
    hexNums = hexPyramidNums();
    echo(hexNums);
    for (i = [0:(len(hexNums) - 1)]) {
        h = hexNums[i];
        echo("HEX#", h);
        makeHexFastLens(h);
    }
}
if (0) {
    pentNums = pentPyramidNums();
    echo(pentNums);
    for (i = [0:(len(pentNums) - 1)]) {  //(len(pentNums) - 1)]) {
        p = pentNums[i];
        echo("PENT#", p);
        makePentSlowLens(p);  //// FIXME slow lenses not in the right position
    }
}

module bar() {
for (pyramidNum = [1:1]) {
    n = NORMALS[pyramidNum];
    normal = quantizeNormal(n);
    angle = acos(normal.z);
    axis = (normal == [0, 0, -1]) ? [1, 0, 0] : [-normal.y, normal.x, 0];
    f = len(FACES[pyramidNum]);
    echo("N: ", pyramidNum, "F: ", f);
    c = (f == 6) ? HEX_FAST_COLOR : PENT_FAST_COLOR;
//    difference() {
        echo("angle: ", angle, "axis: ", axis);
        rotate(a=angle, v=axis)
            color(c, 0.75)
                if (f == 6) {
                    rotate([0, 0, 30])
                        makeHexFastLensComponent();
                } else {
                    rotate([0, 0, 180])
                        makePentFastLensComponent();
                }
        makeMaxPyramid(pyramidNum);
//        sphere(d=LENS_INNER_DIAMETER);
//    }
}
}


//PENT:[2, 3, 8, 9, 16, 17, 18, 19, 22, 26, 28, 29]
//HEX: [0, 1, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 20, 21, 23, 24, 25, 27, 30, 31]

//makeHexSlowLens(0);
makePentSlowLens(3);
