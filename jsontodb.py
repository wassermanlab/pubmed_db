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
   db = __get_database(params['database'])

   #Creating collections & insert data
   pm_collection = get_collection(db.pubmed_id, params['pubmedid_json'])

   gene_collection = get_collection(db.gene_id, params['geneid_json'])


def __get_database(newdbname):
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://user:pass@cluster.mongodb.net/myFirstDatabase"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client[newdbname]


def get_collection(collection, jsonfile):
   with gzip.open(jsonfile) as json:
      json_data = json.load(json)

   collection.insert_many(json_data)

   return collection


if __name__ == "__main__":
    main()