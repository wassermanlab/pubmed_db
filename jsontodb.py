import os
import sys
import pandas as pd
import gzip
import json

from pymongo import MongoClient

import click

CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}

@click.command(no_args_is_help=True, context_settings=CONTEXT_SETTINGS)
@click.option(
    "-d", "--database",
    help="Database name.",
    type=str,
    required=True
)

@click.option(
    "-p", "--pubmedid-json",
    help="Path to Pubmed ID JSON.",
    type=str,
    required=True
)

@click.option(
    "-g", "--geneid-json",
    help="Path to Gene ID JSON.",
    type=str,
    required=True
)


def main(**params):
   ## TODO: Create local MongoDB database - update the get_database function
   db = get_database("somedatabasename")

   ## TODO: Creating collections & insert data (pubmed, gene)
   ## The codes below may be incorrect, please check (these are just preliminary)
   pm_collection = get_collection(db.pubmed_id, params['pubmedid_json'])

   gene_collection = get_collection(db.gene_id, params['geneid_json'])


# function to create local database on server (may eventually want to host it but test with local database first)
def get_database(dbname):

   return dbname

# function to takke collection and insert with json information
def get_collection(collection, jsonfile):
   with gzip.open(jsonfile) as json:
      json_data = json.load(json)

   collection.insert_many(json_data)

   return collection


if __name__ == "__main__":
    main()