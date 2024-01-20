# TruncatedIcosohedron

Package that generates the geometry for a truncated icosohedron

## openSCAD

### Links
* Cheatsheet
  - https://openscad.org/cheatsheet/

### Cartesian Oval Generation

* Values
  - key coordinates
    * (0, R): detonator location
    * (0, 0): pit location
  - circumradius values
    * r_h: hexagon circumradius
    * r_p: pentagon circumradius
  - apical angles (invariant under R) of the hexagonal and pentagonal cones:
    * Θ1 = 2θ1 ∼ 47.60036521 degrees
    * Θ2 = 2θ2 ∼ 40.15350256 degrees
  - explosive velocities
    * v_f (CompB):   8050 m/s
    * v_s (Baratol): 4900 m/s
  - ratio of explosive velocities: (n / m) = (v_f / v_s)
    * no loss of generality if assume m = 1
    * n = (23 / 14)
  - Cartesian Oval formula: (m * p_1) + (n * p_2) = k
    * https://mathworld.wolfram.com/CartesianOvals.html
    * 0 < r < 1
    * m * sqrt(x^2 + (y − R)^2) + n * sqrt(x^2 + y^2) = k
      - sqrt(x^2 + (y − R)^2) + (23 / 14) * sqrt(x^2 + y^2) = k


**FIXME

(Pent:
  Radius: 463.55,
  Sides: 5,
  Pyramid Height: 435.3817447722424,
  EdgeSize: 187.0647738279809,
  Vertices: [[159.12680107096347, 0.0, 435.3817447722424],
             [49.172885791449296, 151.3385810757424, 435.3817447722424],
             [-128.736286326931, 93.53238691399046, 435.3817447722424],
             [-128.73628632693104, -93.53238691399042, 435.3817447722424],
             [49.17288579144926, -151.33858107574244, 435.3817447722424], [0, 0, 0]],
  Faces: [[5, 0, 1], [5, 1, 2], [5, 2, 3], [5, 3, 4], [5, 4, 0], [0, 1, 2, 3, 4]])

**FIXME

(Hex:
  Radius: 463.55,
  Sides: 6,
  Pyramid Height: 424.1289578567895,
  EdgeSize: 187.0647738279809,
  Vertices: [[187.06477382798093, 0.0, 424.1289578567895],
             [93.53238691399048, 162.00284628822186, 424.1289578567895],
             [-93.53238691399042, 162.0028462882219, 424.1289578567895],
             [-187.06477382798093, 2.290882765016604e-14, 424.1289578567895],
             [-93.53238691399055, -162.00284628822183, 424.1289578567895],
             [93.53238691399048, -162.00284628822186, 424.1289578567895], [0, 0, 0]],
  Faces: [[6, 0, 1], [6, 1, 2], [6, 2, 3], [6, 3, 4], [6, 4, 5], [6, 5, 0], [0, 1, 2, 3, 4, 5]]')
## FIXME
