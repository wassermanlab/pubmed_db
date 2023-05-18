import os
import sys
import pandas as pd
import gzip
import json

from pymongo import MongoClient
from jsontodb import __get_database


import click

CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}

@click.command(no_args_is_help=True, context_settings=CONTEXT_SETTINGS)
@click.option(
    "-f", "--foreground",
    help="Foreground genes file.",
    type=str,
    required=True
)

@click.option(
    "-b", "--background",
    help="Background genes file.",
    type=str,
    required=True
)

@click.option(
    "--input-type",
    help="Input type.",
    type=click.Choice(["entrezid", "symbol"], case_sensitive=False),
    default="entrezid",
    show_default=True
)

def main(**params):

    # TODO: Connect to database (the next 3 lines are placeholders)
    db = __get_database('pubmeddb')
    pm_collection = db.pubmed_id
    gene_collection = db.gene_id

    # Identifiers
    foreground = get_identifiers(params["foreground"], params["input_type"])
    background = get_identifiers(params["background"], params["input_type"])

    # Identifiers to PMIDS
    fore_entrezids, fore_symbols, fore_pmids = identifier2pmids(foreground, gene_collection, params['input_type'])
    back_entrezids, back_symbols, back_pmids = identifier2pmids(background, gene_collection, params['input_type'])

    # TODO: From pmids, collect words from the pm_collection and then calculate tfidfs from foreground and background (maybe another function?)


def get_identifiers(input_file, input_type):

    # Get identifiers
    if input_file is not None:
        identifiers = []
        handle = input_file
        for line in handle:
            identifiers.append(line.strip("\n"))
        handle.close()
    if input_type == "entrezid":
        identifiers = list(map(int, identifiers))

    return(identifiers)


def identifier2pmids(idlist, collection, input_type):
    entrezid_list = []
    symbol_list = []
    pmids_list = []


    if input_type == 'entrezid':
        for id in idlist:
            d = collection.find({ "GeneID": id})[0]
            entrezid_list.append(d['GeneID'])
            symbol_list.append(d['Symbol'])
            pmids_list.append(d['PubMed_ID'])
    else:
        for id in idlist:
            d = collection.find({ "Symbol": id})[0]
            symbol_list.append(d['Symbol'])
            entrezid_list.append(d['GeneID'])
            pmids_list.append(d['PubMed_ID'])

    return(entrezid_list, symbol_list, pmids_list)





if __name__ == "__main__":
    main()