#! /bin/bash

#PBS -l walltime=24:00:00,select=1:mem=100gb
#PBS -A st-wasserww-1
#PBS -m ae
#PBS -M <email>

source ~/.bashrc
conda activate pubmeddb

TMPDIR=$PBS_O_WORKDIR

python /project/st-wasserww-1/PubMed_DB/infotojson.py -o $TMPDIR


