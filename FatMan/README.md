# FatMan

* notes
  - use explLenses.py to generate polygon that is the profile for the hexagonal and pentagonal slow explosive lens
    * generates a .scad file with the points for the polygons
  - use explLenses.scad to generate the three types of explosive lenses for both the hexagonal and pentagonal pyramids
    * spin the polygons around the z-axis to make the slow lenses
  - from openscad, save each of the explosive shapes as .csg files
    * explosive shapes (for both hex and pent): booster, slow lens, fast lens, and combined fast and slow lens
  - open the .csg files with freecad and save each shape in .step format
  - open each .step file with Fusion360 and save in the Cad Tools folder
