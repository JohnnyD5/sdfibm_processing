#!/bin/bash
for xdir in case*; do
    cd $xdir
    blockMesh
    touch view.foam
    #qsub job.pbs
    sdfibm > log.txt &
    cd ..
done
