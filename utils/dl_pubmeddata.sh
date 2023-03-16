#! /bin/bash

##Script to download the newest pubmed data annually

#download PubMed Baseline
wget --no-verbose --no-parent --recursive ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/

#download gene2pubmed
wget --no-verbose --no-parent --recursive -O ./utils/data/gene2pubmed.gz ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2pubmed.gz

#get stopwords
wget -O ./utils/data/stopwords-en.txt https://raw.githubusercontent.com/stopwords-iso/stopwords-en/master/stopwords-en.txt

#download geneinfo
wget --no-verbose --no-parent --recursive -O ./utils/data/Homo_sapiens.gene_info.gz ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz
