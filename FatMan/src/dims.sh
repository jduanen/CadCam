#!/bin/bash
#
# Script to get the radius measurements for the Gadget's layers

OUT_FORMAT="--opprint"  # --ojson
NUM_LINES=13
IN_FILE="${HOME}/CadCam/FatMan/src/Gadget Data - Dimensions.csv"

mlr --csv ${OUT_FORMAT} head -n ${NUM_LINES} then cut -f Component,Radius "${IN_FILE}"
