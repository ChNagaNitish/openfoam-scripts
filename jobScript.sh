#! /bin/bash
#
#SBATCH -t 6-00:00:00
#SBATCH -N 5
#SBATCH --ntasks 480
#SBATCH --account=cavitation
#SBATCH -p normal_q
#SBATCH --mail-user=naga@vt.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=les

# Loading required modules for OpenFOAM and Postprocessing
module purge
module reset
module load GCC/13.3.0 OpenMPI/5.0.3-GCC-13.3.0 boost/1.77.0 FFTW/3.3.10-GCC-13.3.0 Bison/3.8.2-GCCcore-13.3.0
source $HOME/opt/v2112/OpenFOAM-v2112/etc/bashrc
export FOAM_FILEHANDLER=collated
export FOAM_IORANKS='(0 96 192 288 384)'
#Changing the subdomains for decomposition of mesh based on number of processes specified
sed -i "17s/.*/numberOfSubdomains $SLURM_NTASKS;/" system/decomposeParDict
# Decomposing the domain
decomposePar
# Running the solver in parallel mode
mpirun -np $SLURM_NTASKS myInterPhaseChangeFoam -parallel > residuals2.log
# Reconstructing the domain from the subdomains after the simulation is done
reconstructPar #&& rm -r processor*


# Change 'switch' To 'true' to start postprocessing after the simulation is done
switch=false
if [ "$switch" = "true" ]; then
	sbatch ~/globalScripts/parallelPostProcessing.sh
fi
#
echo "Normal end of execution."
