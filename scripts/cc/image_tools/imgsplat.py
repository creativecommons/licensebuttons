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

def load_graph(filename):
    """Load the specified filename; return a graph."""

    store = Graph()
    store.bind("cc", "http://creativecommons.org/ns#")
    store.bind("dc", "http://purl.org/dc/elements/1.1/")
    store.bind("dcq","http://purl.org/dc/terms/")
    store.bind("rdf","http://www.w3.org/1999/02/22-rdf-syntax-ns#")

    store.load(filename)

    return store

def copyto(source, dest, code, size, jurisdiction, money):
    if (not os.access(dest, os.F_OK)):
	os.makedirs(dest)
    dest += size+'.png'
    if string.find(code, 'nc') != -1 and money.has_key(jurisdiction):
	source += '_'+money[jurisdiction]
    source += '.png'
    try:
	shutil.copy2(source, dest)
    except:
	print 'Failed to copy '+source+' to '+dest

def splat(license_graph):

    money = {
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
        'pt': 'euro',
    }

    for uri in license_graph.subjects(NS_RDF.type, NS_CC.License):
        print uri
	m = re.search('http://creativecommons.org/licenses/(.*?)/((.*?)/((.*?)/)?)?', str(uri))
	code = m.group(1)
	version = m.group(3)
	jurisdiction = m.group(5)
	dest = '../www/l/'+code+'/'
	code2 = code
	size = '88x31'
	if (code == 'by-nd-nc'):
	    code2 = 'by-nc-nd'
	elif (code == 'nc' or code == 'nd' or code == 'sa' or code == 'nd-nc' or code == 'nc-sa'):
	    code2 = 'somerights1'
	elif (code == 'LGPL' or code == 'GPL'):
	    size = '88x62'
        if (version):
	    dest += version+'/'
        if (jurisdiction):
	    dest += jurisdiction+'/'
	source = '../base-images/'+size+'/'+code2
	copyto(source, dest, code, size, jurisdiction, money)
	source = '../base-images/'+'80x15'+'/'+code2
	copyto(source, dest, code, '80x15', '', money)

def cli():
    """imgsplat command line interface."""

    splat(load_graph('http://creativecommons.org/licenses/index.rdf'))
