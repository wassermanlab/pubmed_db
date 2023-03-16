#!/usr/bin/env python

import os
import sys
import pandas as pd
import gzip
import json
from datetime import date

import xml.etree.ElementTree as ET
from utils.abstract2words import __get_abstract_words

import click

CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}

@click.command(no_args_is_help=True, context_settings=CONTEXT_SETTINGS)
@click.option(
    "-o", "--output-dir",
    help="Output directory. [Default: current workding directory]",
    type=str
)

@click.option(
    "-i", "--pubmed-dir",
    help="Path to baseline directory from current script directory. [Default: ./ftp.ncbi.nlm.nih.gov/pubmed/baseline/]",
    type=str,
    default="./ftp.ncbi.nlm.nih.gov/pubmed/baseline/"
)

@click.option(
    "-y", "--year",
    help="Year of PubMed Database. [Default: Current Year]",
    type=int
)

@click.option(
    "-t", "--taxonomy",
    help="Taxonmy to keep for gene2pubmed. [Default: 9606]",
    type=int
)


def main(**params):

    #SetUp
    os.chdir(sys.path[0]) #change working dir to where this file is
    inputdir = os.getcwd()

    datadir = os.path.join(inputdir, 'utils/data/')
    if not os.path.isdir(datadir):
        print("Please download necessary files using dl_pubmeddata.sh")
        exit
  
    pubmed_dir = os.path.join(inputdir, params['pubmed_dir'])
    if not os.path.isdir(pubmed_dir):
        print("Please download necessary files using dl_pubmeddata.sh")
        exit

    if not params['output_dir']:
        outdir = os.getcwd()
    else:
        outdir = params['output_dir']

    if not params['year']:
        year = date.today().year
    else:
        year = params['year']

    tax = params['taxonomy']

    #Download necessary files
    gene2pubmed_file = os.path.join(datadir, 'gene2pubmed.gz')

    if not os.path.exists(gene2pubmed_file):
        print("Please download necessary files using dl_pubmeddata.sh")
        exit
    else:
        human_gene2pm = pd.read_table(gene2pubmed_file, sep="\t", header=0, 
            names=['TaxID', 'GeneID', 'PubMed_ID']).query('TaxID == @tax')
              
        human_pmids = set(human_gene2pm['PubMed_ID'])


    geneinfo_file = os.path.join(datadir, 'Homo_sapiens.gene_info.gz')
    if not os.path.exists(geneinfo_file):
        print("Please download necessary files using dl_pubmeddata.sh")
        exit
    else:
        human_geneinfo = pd.read_table(geneinfo_file, sep="\t", header=0, usecols=[0,1,2], 
                                       names=['TaxID', 'GeneID', 'Symbol']).query('TaxID == @tax').drop(columns=['TaxID'])
    

    #Convert genes to JSON
    agg_humangene2pm = pd.DataFrame(human_gene2pm.groupby('GeneID')["PubMed_ID"].agg(list)).reset_index().merge(human_geneinfo)

    genejsontofile = agg_humangene2pm[['GeneID', 'Symbol', 'PubMed_ID']].to_dict('records')

    genejson_file = os.path.join(outdir, 'gene2pubmedid.json.gz')  
    with gzip.open(genejson_file, 'wt') as genejson_file:
        json.dump(genejsontofile, genejson_file, indent=4) 


    #For Pubmed files, Only use the actual XML files, not the md5 files
    xmllist = []
    for x in os.listdir(pubmed_dir):
        if x.find('md5') == -1 and x.find('README') == -1: #does not find md5
            xmllist.append(x)

    xmllist = sorted(xmllist)

    #Convert to xml to JSON
    pmjsontofile = []

    for xml in xmllist:
        print(f'Working on: {xml}')
        pmtojson = xmltolistdict(xml, human_pmids)

        pmjsontofile.extend(pmtojson)
        print('Updated object')

    pmjson_file = os.path.join(outdir, f'pubmeddb_{year}.json.gz')  
    with gzip.open(pmjson_file, 'wt') as pmjson_file:
        json.dump(pmjsontofile, pmjson_file, indent=4)


def xmltolistdict(x, human_pmids):
    included_pmids = set()
    tojson = []

    #SETTING UP FIELDS THAT WE CARE ABOUT
    tagswanted = ["PMID", "Language", "JournalTitle", "ArticleTitle", "AbstractText", "MedlineJournalInfo", "Country", "ChemicalList", "RegistryNumber", "MeshHeadingList", "DescriptorName", "QualifierName"]
    tagswantedeasy = ["JournalTitle", "ArticleTitle"]

    input = gzip.open(os.path.join('./ftp.ncbi.nlm.nih.gov/pubmed/baseline/', x), 'r')
    tree = ET.parse(input)
    root = tree.getroot()

    #Need to find the entries to the correct pubmed ids
    for pmset in root:
        for pm in pmset: #iterate thru pubmed article
            pmdict = {} #create empty dictionary to add fieldes -> JSON
            pmid = False
            eng = False
            passedmedline = False
            
        
            for elem in pm.iter():
                # tags.add(elem.tag) #Obtain only the tags for the XML file
            
                if (elem.tag in tagswanted):
                    if (elem.tag in tagswantedeasy):
                        pmdict[elem.tag] = elem.text

                    elif (elem.tag == "PMID"):
                        if int(elem.text) in human_pmids: #filter
                            pmid = int(elem.text)
                            pmdict[elem.tag] = pmid
                        else: #if PubMedID not wanted, can end here (don't need to iterate)
                            break

                    elif (elem.tag == "Language"):
                        if (elem.text == "eng"):
                            eng = True
                        else: #if not english, can end here (don't need to iterate)
                            break
                
                    elif (elem.tag == "AbstractText"):
                        abstract = elem.text
                        wordsdict = dict()

                        try:
                            for word, stems, count in __get_abstract_words(abstract, True, True):
                                wordsdict[word] = {'Stems':stems, 'Count':count}
                        except:
                            print(f"PMID ID:{pmid} - Error in getting abstract words")

                        abstractdict = {'Text': abstract, 'Words':wordsdict}
                        pmdict['Abstract'] = abstractdict
        
                    elif (elem.tag == "MedlineJournalInfo"):
                        passedmedline = True

                    elif (elem.tag == "Country" and passedmedline):
                        pmdict[elem.tag] = elem.text

                    elif (elem.tag == "ChemicalList"):
                        chemicallist = [] #could change this to set if don't want to duplicate

                    elif (elem.tag == "RegistryNumber"):
                        chemicallist.append(elem.text)
                        pmdict['RegistryNumber'] = chemicallist
                
                    elif (elem.tag == "MeshHeadingList"):
                        meshdict = {}
                        pmdict['MeshHeading'] = meshdict
                    
                    elif (elem.tag == "DescriptorName"):
                        descdict = {elem.tag: elem.text}
                        meshdict[elem.attrib['UI']] = descdict
                        qualdict = {}
                    
                    elif (elem.tag == "QualifierName"):
                        qualdict[elem.attrib['UI']] = elem.text
                        descdict['QualifierName'] = qualdict

            if pmid != False and eng:
                included_pmids.add(pmid)
                tojson.append(pmdict)

    return(included_pmids, tojson)

if __name__ == "__main__":
    main()
