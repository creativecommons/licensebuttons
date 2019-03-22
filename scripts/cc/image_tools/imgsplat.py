"""
imgsplat.py

(c) 2006 Creative Commons.
"""

__version__ = 0.1

import os
import re
import shutil
import string

from rdflib.Graph import Graph
from rdflib import Namespace

NS_CC = Namespace("http://creativecommons.org/ns#")
NS_RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
NS_FOAF = Namespace("http://xmlns.com/foaf/0.1/")

MONEY = {
    'at': 'euro',
    'be': 'euro',
    'fi': 'euro',
    'de': 'euro',
    'es': 'euro',
    'fr': 'euro',
    'gr': 'euro',
    'ie': 'euro',
    'it': 'euro',
    'lu': 'euro',
    'nl': 'euro',
    'pt': 'euro'}


def checkout_base():
    """Return the base destination path.  Note that this assumes you're
    running the tool from a Subversion checkout (or that your filesystem
    layout is the same as our repository)."""


    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', '..')
        )

def load_graph(filename):
    """Load the specified filename; return a graph."""

    store = Graph()
    store.bind("cc", "http://creativecommons.org/ns#")
    store.bind("dc", "http://purl.org/dc/elements/1.1/")
    store.bind("dcq","http://purl.org/dc/terms/")
    store.bind("rdf","http://www.w3.org/1999/02/22-rdf-syntax-ns#")

    store.load(filename)

    return store

def copyto(source, dest, code, size, jurisdiction, money=MONEY):
    # Make the destination directory, if necessary
    dest_dir = os.path.dirname(dest)
    if (not os.access(dest_dir, os.F_OK)):
        os.makedirs(dest_dir)

    # If NC (and not the 80x15 icon), use the appropriate currency icon.
    if ((string.find(code, 'nc') != -1
         and money.has_key(jurisdiction)
         and size != '80x15'
         and not 'somerights1' in source)):
        source += '_' + money[jurisdiction]

    source += '.png'

    try:
        shutil.copy2(source, dest)
    except:
        print 'Failed to copy '+source+' to '+dest


def splat(license_graph):
    for uri in license_graph.subjects(NS_RDF.type, NS_CC.License):
        print uri

        for s, p, logo in license_graph.triples((uri, NS_FOAF.logo, None)):
            # Get the dest_path, which is base-images and
            # everything after 'http://i.creativecommons.org/'
            dest_path = os.path.join(
                checkout_base(), 'www', str(logo)[29:])

            m = re.search(
                '^http://i.creativecommons.org/'
                '(?P<group>l|p)/'
                '(?P<code>.*?)/'
                '((?P<version>.*?)/'
                '((?P<jurisdiction>.*?)/)?)?'
                '(?P<size>.*)\.png$', str(logo))

            code = m.group('code')
            jurisdiction = m.group('jurisdiction')
            size = m.group('size')

            code2 = code
            if (code == 'by-nd-nc'):
                code2 = 'by-nc-nd'
            elif code in ('nc', 'nd', 'sa', 'nd-nc', 'nc-sa'):
                code2 = 'somerights1'

            source = os.path.join(
                checkout_base(), 'base-images', size, code2)

            copyto(source, dest_path, code, size, jurisdiction)


def cli():
    """imgsplat command line interface."""

    splat(load_graph('http://creativecommons.org/licenses/index.rdf'))
