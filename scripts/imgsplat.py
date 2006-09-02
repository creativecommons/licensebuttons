"""
imgsplat.py

Requires lxml (http://codespeak.net/lxml).

(c) 2006 Creative Commons.
"""

__version__ = 0.1

import lxml.etree

import re
import string

def splat(instream):

    money = { 'es': 'euro', 'jp': 'yen' }

    licenses = lxml.etree.parse(instream)
    uris = licenses.xpath('//jurisdiction/version/@uri')
    for uri in uris:
        print uri
	m = re.search('http://creativecommons.org/licenses/(.*?)/((.*?)/((.*?)/)?)?', uri)
	code = m.group(1)
	version = m.group(3)
	jurisdiction = m.group(5)
	dest = '../www/l/'+code+'/'
	source = code
        if (version):
	    dest += version+'/'
        if (jurisdiction):
	    dest += jurisdiction+'/'
	dest += '88x31.png'
	print dest
	#if string.find(code, 'nc') != -1 and money.has_key(jurisdiction):
	#    source += '_'+money[jurisdiction]
	source += '.png'
	print source
     
if __name__ == '__main__':
    splat(file('api_xml/licenses.xml'))
