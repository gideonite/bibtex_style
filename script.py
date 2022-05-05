#! /usr/bin/python3

import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import as_text

import os, sys

# TODO(dresdner) How to handle DOI? DOI > url? 

def get_url(bib_entry):
    try:
        return bib_entry['url']
    except KeyError:
        print("failed on", bib_entry['title'])
        return None


def process_entry(bib_entry):
    url = get_url(bib_entry)
    new_entry = bib_entry.copy()

    if url is not None:
        title = bib_entry['title']
        title_with_url = f"\href{{{url}}}{{{title}}}"
        new_entry['title'] = title_with_url

    delete_keys = ['url', 'abstract', 'pages', 'language', 'urldate', 'pages', 'keywords', 'note', 'number']
    for k in delete_keys:
        try:
            del new_entry[k]
        except KeyError:
            pass

    return new_entry


def process_bib(bib_db):
    new_entries = [process_entry(entry) for entry in bib_db.entries]
    bib_db.entries = new_entries
    return bib_db


def main():
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        processed = process_bib(bibtexparser.load(f))

    writer = BibTexWriter()
    sys.stdout.write(writer.write(processed))


if __name__ == '__main__':
    main()
