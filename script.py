#! /usr/bin/python3

import bibtexparser
from bibtexparser.bwriter import BibTexWriter

import os, sys

# TODO(dresdner) How to handle DOI? DOI > url? 

def get_url(bib_entry):
    try:
        return bib_entry['url']
    except KeyError:
        print("failed on", bib_entry['title'])
        return None


def process_entry(bib_entry, delete_keys=['pages', 'language', 'number', 'url']):
    url = get_url(bib_entry)
    new_entry = bib_entry.copy()

    if url is not None:
        title = bib_entry['title']
        title_with_url = f"\href{{{url}}}{{{title}}}"
        new_entry['title'] = title_with_url

    for k in delete_keys:
        if k in new_entry:
            del new_entry[k]

    return new_entry


def process_bib(bib_db):
    new_entries = [process_entry(entry) for entry in bib_db.entries]
    bib_db.entries = new_entries
    return bib_db


def main():
    if len(sys.argv) == 1:
        print("usage: script.py (file name) [additional file names]")

    filenames = sys.argv[1:]
    for filename in filenames:
        with open(filename, 'r') as f:
            parser = bibtexparser.bparser.BibTexParser(common_strings=True).parse_file
            processed = process_bib(parser(f))

        writer = BibTexWriter()
        sys.stdout.write(writer.write(processed))

if __name__ == '__main__':
    main()
