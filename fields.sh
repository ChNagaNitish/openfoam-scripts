#!/bin/bash
pvbatch="$HOME/opt/ParaView-5.13.2-MPI-Linux-Python3.10-x86_64/bin/pvbatch"
threeD=$1
fieldExtract="${pvbatch} $HOME/globalScripts/openfoam-scripts/fieldExtract.py"
fieldProcess="python3 $HOME/globalScripts/openfoam-scripts/fieldProcess.py ${threeD}"
if [ -d "system" ]; then
	$fieldExtract
	$fieldProcess
	printf '\n.................... Done Post-processing %s ....................\n\n' "${PWD##*/}"
else
	printf "\nERROR....................'%s' is not a case directory\n" "${PWD##*/}"
fi
