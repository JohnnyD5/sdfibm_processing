#!/bin/bash
for xdir in case*; do
    cd $xdir
    qsub job.pbs
    cd ..
done
