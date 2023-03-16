<strong>README</strong>
=====
Instructions on how to update the PubMedDB annually.


Table of Contents
-----
1. [Conda](#conda-environment)
2. [Download PubMed Baseline](#baseline)
3. [XML to JSON](#xml-to-json)


Conda Environment
-----
All packages are provided within the YML environment file. A conda environment named `pubmeddb` can be created using the following command.
```bash
conda env create -f ./pubmeddb.yml
```
<br>
<br>

Baseline
-----
Please use the <strong>DATA TRANSFER node</strong> of Sockeye to download the PubMed baseline (https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/) and gene2pubmed (https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2pubmed.gz).
```bash
ssh <cwl>@dtn.sockeye.arc.ubc.ca
```
<br>

Run download script:
```bash
bash ./utils/dl_pubmeddata.sh
```
<br>
<br>

XML to JSON
-----
Please edit the `PBS -M` with your email address in `pubmed_submit.sh`.
```bash
##PBS -M <email>
```
<br>
Run the following code in the <strong>COMPUTE node</strong> and submit script as a job from a tempory/scratch directory (currently project directory is only readbale byt the compute nodes).

```bash
cd <SCRATCH DIR>
qsub /project/st-wasserww-1/PubMed_DB/pubmed_submit.sh
```







