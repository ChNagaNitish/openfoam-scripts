#! /bin/bash
#
#SBATCH -t 0-01:00:00
#SBATCH -N 1
#SBATCH -n 3
#SBATCH --account=cavitation
#SBATCH -p normal_q
#SBATCH --mail-user=naga@vt.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=postparallel
#
#

#Loading Required Scripts
postPath="$(dirname "$(realpath "$0")")"
fields="$postPath/fields.sh"
combine="$postPath/combine.py"

#Moving time folders to subfolders
echo "Started copying the time folders into proc folders"
dirList=($(find . -maxdepth 1 -type d -name "[0-9]*\.[0-9]*" -printf "%f\n" | sort -n))
timeFolders=${#dirList[@]}
perProc=$(expr $timeFolders / $SLURM_NTASKS)
prefix="proc_"
begin=0

for i in $(seq 1 $SLURM_NTASKS)
do
	mkdir -p "$prefix$i"
	cp -r "system" "$prefix$i/"
	cp -r "constant" "$prefix$i/"
done

for i in $(seq 1 $SLURM_NTASKS)
do
	srun -Q --exclusive -n 1 -N 1 bash -c "$postPath/copyDirectories.sh $begin $prefix$i $SLURM_NTASKS $perProc $i" &
	begin=$((perProc * i))
done
wait
echo "Done copying time folders"


#Processing each folder simultaneously
echo "Started extracting data"
for i in $(seq 1 $SLURM_NTASKS)
do
	cd "./proc_$i"
	srun -Q --exclusive -n 1 -N 1 "$fields" &
	cd ..
	sleep 1
done
wait
echo "Done extracting and processing data in the proc folders"

echo "Started combining parquet files from proc folders into single one"
#Making results folder
mkdir -p results/data/All

#Combining the individual Pandas DF into one
python3 "$combine" $SLURM_NTASKS && $postPath/deleteParallel.sh
wait
echo "Completed Post-processing the results parallelly"