# sdfibm_ellipse
Contains python files to do data analysis
# workstation
```
ssh -X zhizhong@130.39.39.248
```
Go to the folder
```
python gen_cases
```
```
bash runall.sh
```

# QB
The python file will auto-generate the job.pbs files for all folders

*runall_qb* is used to submit jobs

One thing to keep in mind: each work is done in just one processor.

So we just use single node with 1 ppn

if we allocate more, but don't decompose the case, all unused processors will be idle, giving a warning of wasting resources

To run sdfibm on hpc, add this line to the ~/.bashrc file
```
export PATH=$PATH:~/sdfibm/src
```
# Running Difference
* `runall.sh` file:  there are two runall files  
1. For single processor test:
```
#!/bin/bash
for xdir in case*; do
    cd $xdir
    blockMesh
    touch view.foam
    #qsub job.pbs
    sdfibm > log.txt &
    cd ..
done
```

2. For multiple processors
```
#!/bin/bash
for xdir in case*; do
    cd $xdir
    blockMesh
    decomposePar -force
    touch view.foam
    #qsub job.pbs
    mpirun -np 10 sdfibm -parallel > log.txt &
    cd ..
done
```

* About purge file:
1. For most uses, we use purge file in system controlDict file

```
/*--------------------------------*- C++ -*----------------------------------*\
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  6.0                                 |
|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "system";
    object      controlDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
application     ibm;

startFrom       startTime;

startTime       0.0;

stopAt          endTime;

endTime         300;

deltaT          0.001;

writeControl    runTime;

writeInterval   1;

purgeWrite      5;

writeFormat     binary;

writePrecision  6;

writeCompression off;

timeFormat      general;

timePrecision   6;

runTimeModifiable false;
adjustTimeStep no;

functions
{
	forces1
	{
   	 // Mandatory entries
   	 type            forces;
   	 functionObjectLibs ( "libforces.so" );
   	 patches         (top);
	   writeControl    runTime;
	   writeInterval   1;

    	// Optional entries

   	 // Field names
   	 pName               p;
   	 UName               U;
   	 rho             rhoInf;
	   rhoInf              1;

    	// Reference pressure [Pa]
    	pRef            0;

    	// Include porosity effects?
    	porosity        no;

    	// Store and write volume field representations of forces and moments
    	writeFields     yes;

    	// Centre of rotation for moment calculations
   	 CofR            (0 0 0);

    	// Spatial data binning
   	 // - extents given by the bounds of the input geometry
   	 //binData
    	 //{
   	 //   nBin        20;
   	 //  direction   (1 0 0);
    	//   cumulative  yes;
   	// }
	}

	forces2
	{
   	 // Mandatory entries
   	 type            forces;
   	 functionObjectLibs ( "libforces.so" );
   	 patches         (bottom);

	writeControl    runTime;
        writeInterval   1;
    	// Optional entries

   	 // Field names
   	 pName               p;
   	 UName               U;
   	 rho             rhoInf;
	   rhoInf              1;

    	// Reference pressure [Pa]
    	pRef            0;

    	// Include porosity effects?
    	porosity        no;

    	// Store and write volume field representations of forces and moments
    	writeFields     yes;

    	// Centre of rotation for moment calculations
   	 CofR            (0 0 0);

    	// Spatial data binning
   	 // - extents given by the bounds of the input geometry
   	 //binData
    	 //{
   	 //   nBin        20;
   	 //  direction   (1 0 0);
    	//   cumulative  yes;
   	// }
	}
}
```
2. Normally, if you want data of all times, `purgeWrite` should be `0`

# decomposePar error
size 240000 is not equal to the given value of 320000
## Solving method
delete AS file in 0 folder
# Remove all post processing files
```
rm -rf process*
```
