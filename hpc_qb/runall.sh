#!/bin/bash
for xdir in case*; do
    cd $xdir
    touch view.foam
    qsub job.pbs
    cd ..
done
