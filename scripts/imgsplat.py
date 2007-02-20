"""
imgsplat.py

Requires lxml (http://codespeak.net/lxml).

(c) 2006 Creative Commons.
"""

__version__ = 0.1

import lxml.etree

import os
import re
import shutil
import string

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

def splat(instream):

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

    licenses = lxml.etree.parse(instream)
    uris = licenses.xpath('//jurisdiction/version/@uri')
    for uri in uris:
        print uri
	m = re.search('http://creativecommons.org/licenses/(.*?)/((.*?)/((.*?)/)?)?', uri)
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
     
if __name__ == '__main__':
    splat(file('api_xml/licenses.xml'))
