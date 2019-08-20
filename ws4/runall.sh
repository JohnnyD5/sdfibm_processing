#!/bin/bash
for xdir in case*; do
    cd $xdir
	touch view.foam
    sdfibm > log.txt &
    cd ..
done
