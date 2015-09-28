""" Command line tool to get an Odoo model collection and output in JSON format
"""
from odoo_model_collection import OdooModelCollection
from html_formatter import HTMLFormatter
import argparse
import sys
import os
import errno


PARSER = argparse.ArgumentParser(description='Quick JSON file generator '
                                             'containing model schema of the '
                                             'provided Odoo DB - eg -d <dbname>'
                                             ' -u <username>')
PARSER.add_argument('-s', help='URL of the Odoo server '
                               '(default: http://localhost:8069)',
                    default='http://localhost:8069')
PARSER.add_argument('-d', help='Name of the database to connect to '
                               '(default: openerp)',
                    default='openerp')
PARSER.add_argument('-u', help='Username to use when connecting to the '
                               'database (default: admin)', default='admin')
PARSER.add_argument('-p', help='Password to use for username when connecting '
                               'to database (default: admin)', default='admin')
PARSER.add_argument('-f', help='Filter to only get classes that contain '
                               'this string.')
PARSER.add_argument('-o', help='Output a HTML & d3.js version of model '
                               'collection')


def main():
    """ Method to take command line args, get model collection and return JSON
    :return: prints JSON
    """
    args = PARSER.parse_args()
    collection = OdooModelCollection(model_filter=args.f,
                                     db=args.d,
                                     server=args.s,
                                     user=args.u,
                                     password=args.p)
    if not args.o:
        print collection.convert_collection_to_json()
    else:
        html = HTMLFormatter(collection=collection)
        if not os.path.exists(args.o):
            try:
                os.makedirs(args.o)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(args.o):
                    pass
                else:
                    raise
        fname = '{0}.html'.format(args.f if args.f else 'index')
        with open('{0}/{1}'.format(args.o, fname), 'wb') as wfile:
            wfile.write(html.html)


if __name__ == '__main__':
    sys.exit(main())
