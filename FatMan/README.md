# FatMan

An accurate 3D model of the first implosion/plutonium/fission weapon.

## Documentation

This repo includes documentation collected in the process of creating this model.

## 3D Model

The model consists of three major components: the physics package (which includes all of the explosives and fissionable material inside of an spherical aluminum shell), the support functions (including the fireset, the radar, the timer, the barometric sensors, and associated cabling), and the ballistic shell (consisting of the outer casing, tail section, radar antennae, and safeing/arming plugs).

### Physics Package

**TBD**

### Support Functions

**TBD**

### Ballistic Shell

**TBD**

## Tools for Generating the Model

While Fusion360 is the primary tool used to create this model, several other tools were used in order to cre

* notes
  - use explLenses.py to generate polygon that is the profile for the hexagonal and pentagonal slow explosive lens
    * generates a .scad file with the points for the polygons
  - use explLenses.scad to generate the three types of explosive lenses for both the hexagonal and pentagonal pyramids
    * spin the polygons around the z-axis to make the slow lenses
  - from openscad, save each of the explosive shapes as .csg files
    * explosive shapes (for both hex and pent): booster, slow lens, fast lens, and combined fast and slow lens
  - open the .csg files with freecad and save each shape in .step format
  - open each .step file with Fusion360 and save in the Cad Tools folder
