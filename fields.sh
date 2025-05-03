#!/bin/bash

pvbatch="$HOME/opt/ParaView-5.9.1-MPI-Linux-Python3.8-64bit/bin/pvbatch"
fieldExtract="${pvbatch} $HOME/globalScripts/openfoam-scripts/fieldExtract.py"
fieldProcess="python3 $HOME/globalScripts/openfoam-scripts/fieldProcess.py"
if [ -d "system" ]; then
	$fieldExtract
	$fieldProcess
	printf '\n.................... Done Post-processing %s ....................\n\n' "${PWD##*/}"
else
	printf "\nERROR....................'%s' is not a case directory\n" "${PWD##*/}"
fi
