#! /bin/bash
#
#SBATCH -t 0-00:30:00
#SBATCH -N 1
#SBATCH -n 2
#SBATCH --account=cavitation
#SBATCH -p normal_q
#SBATCH --mail-user=naga@vt.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=postparallel
#
#
module load Python/3.12.3-GCCcore-13.3.0
source $HOME/workEnvCPU/bin/activate
#Loading Required Scripts
#postPath="$(dirname "$(realpath "$0")")"
postPath="$HOME/globalScripts/openfoam-scripts"
fields="$postPath/fields.sh"
combine="$postPath/combine.py"
avg="$postPath/averaging.py"
threeD=1

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
	srun -Q --exclusive -n 1 -N 1 bash -c "$fields $threeD" &
	cd ..
	sleep 1
done
wait
echo "Done extracting and processing data in the proc folders"

echo "Started combining parquet files from proc folders into single one"
#Making results folder
mkdir -p results/data

#Combining the individual Pandas DF into one
mv proc_1/results/data/points.parquet resutls/data/
python3 $combine $SLURM_NTASKS && $postPath/deleteParallel.sh
wait
python3 $avg
#echo "Completed Post-processing the results parallelly"
