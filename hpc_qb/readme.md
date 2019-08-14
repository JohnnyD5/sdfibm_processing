This is the package used to run on HPC_QB

The python file will auto-generate the job.pbs files for all folders

*runall* is used to submit jobs

One thing to keep in mind: each work is done in just one processor.

So we just use single node with 1 ppn

if we allocate more, but don't decompose the case, all unused processors will be idle, giving a warning of wasting resources

To run sdfibm on hpc, add this line to the ~/.bashrc file
```
export PATH=$PATH:~/sdfibm/src
```
