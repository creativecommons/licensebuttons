"""Copy license button images into paths named by the license RDF index.

For each ``foaf:logo`` URL on a ``cc:License``, use the URL's license code
and image size to choose a PNG from ``base-images``. Copy that PNG to the
corresponding path under ``www`` so the URL can be served as a static file.
The ``imgsplat`` console command loads the Creative Commons license index.

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

# Jurisdictions whose noncommercial buttons use the local ``_euro`` variant.
MONEY = {
    "at": "euro",
    "be": "euro",
    "fi": "euro",
    "de": "euro",
    "es": "euro",
    "fr": "euro",
    "gr": "euro",
    "ie": "euro",
    "it": "euro",
    "lu": "euro",
    "nl": "euro",
    "pt": "euro",
}


def checkout_base():
    """Return the repository root, three directories above this module.

    The expected layout has ``base-images`` and ``www`` at that root.
    """

    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..")
    )


def load_graph(filename):
    """Parse an RDF file or URL into a graph with common namespace prefixes."""

    store = Graph()
    store.bind("cc", "http://creativecommons.org/ns#")
    store.bind("dc", "http://purl.org/dc/elements/1.1/")
    store.bind("dcq", "http://purl.org/dc/terms/")
    store.bind("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")

    store.load(filename)

    return store


def copyto(source, dest, code, size, jurisdiction, money=MONEY):
    """Copy a source PNG stem to a destination path, selecting a variant.

    ``source`` has no extension; ``dest`` is the complete output filename.
    For supported jurisdictions, noncommercial buttons other than 80x15
    use a currency-suffixed source. Copy failures are reported to stdout
    and do not stop processing.
    """

    # The URL-derived destination may contain directories not yet in www.
    dest_dir = os.path.dirname(dest)
    if not os.access(dest_dir, os.F_OK):
        os.makedirs(dest_dir)

    # The generic somerights1 button has no currency-specific source.
    if (
        string.find(code, "nc") != -1
        and jurisdiction in money
        and size != "80x15"
        and "somerights1" not in source
    ):
        source += "_" + money[jurisdiction]

    source += ".png"

    try:
        shutil.copy2(source, dest)
    except:  # noqa: E722 (FIXME)
        # Flake8 lint runs via Python 3 so skip following E999
        print "Failed to copy", source, "to", dest  # noqa: E999


def splat(license_graph):
    """Copy local button images for the license logo URLs in an RDF graph.

    Only subjects typed ``cc:License`` are visited. Their ``foaf:logo``
    values are expected to be i.creativecommons.org PNG URLs in the
    ``/l/`` or ``/p/`` layout; each URL becomes a path below ``www``.
    """

    for uri in license_graph.subjects(NS_RDF.type, NS_CC.License):
        print uri

        for s, p, logo in license_graph.triples((uri, NS_FOAF.logo, None)):
            # Mirror the path after the image host beneath www.
            dest_path = os.path.join(checkout_base(), "www", str(logo)[29:])

            # A logo URL encodes the license code, optional version and
            # jurisdiction, and the image size used to find a local PNG.
            m = re.search(
                "^http://i.creativecommons.org/"
                "(?P<group>l|p)/"
                "(?P<code>.*?)/"
                "((?P<version>.*?)/"
                "((?P<jurisdiction>.*?)/)?)?"
                r"(?P<size>.*)\.png$",
                str(logo),
            )

            code = m.group("code")
            jurisdiction = m.group("jurisdiction")
            size = m.group("size")

            # Some URL codes share a source image or use a different order
            # from the filenames in base-images.
            code2 = code
            if code == "by-nd-nc":
                code2 = "by-nc-nd"
            elif code in ("nc", "nd", "sa", "nd-nc", "nc-sa"):
                code2 = "somerights1"

            source = os.path.join(checkout_base(), "base-images", size, code2)

            copyto(source, dest_path, code, size, jurisdiction)


def cli():
    """Load the published license index and copy all referenced buttons."""

    splat(load_graph("http://creativecommons.org/licenses/index.rdf"))
