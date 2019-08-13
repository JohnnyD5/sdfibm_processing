#!/bin/bash
for xdir in case*; do
    cd $xdir
    sdfibm > log.txt &
    cd ..
done
