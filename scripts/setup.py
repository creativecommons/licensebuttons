## Copyright (c) 2007 Nathan R. Yergler, Creative Commons

## Permission is hereby granted, free of charge, to any person obtaining
## a copy of this software and associated documentation files (the "Software"),
## to deal in the Software without restriction, including without limitation
## the rights to use, copy, modify, merge, publish, distribute, sublicense,
## and/or sell copies of the Software, and to permit persons to whom the
## Software is furnished to do so, subject to the following conditions:

## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Software.

## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
## FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
## DEALINGS IN THE SOFTWARE.

from setuptools import setup

setup(
    name = "cc.image_tools",
    version = "1.0",
    packages = ['cc.image_tools'],

    entry_points = {'console_scripts' : 
                    ['imgsplat = cc.image_tools.imgsplat:cli',
                     ]
                    },
    
    install_requires = ['setuptools',
                        'rdflib<3.0',
                        ],

    include_package_data = True,
    zip_safe = True,

    author = 'Mike Linksvayer',
    author_email = 'ml@creativecommons.org',
    description = 'Tools for managing i.creativecommons.org.',
    license = 'MIT',
    url = 'http://wiki.creativecommons.org/Developer',

    )
