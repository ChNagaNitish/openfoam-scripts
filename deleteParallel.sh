#!/bin/bash
for i in $(seq 1 $SLURM_NTASKS)
do
	srun -n 1 -N 1 --exclusive bash -c "if [ -d proc_$i ]; then rm -r proc_$i && echo 'Deleted proc_$i'; else echo 'proc_$i not found'; fi" &
done
wait
