""" Command line tool to get an Odoo model collection and output in JSON format
"""
from odoo_models.odoo_model_collection import OdooModelCollection
import argparse
import sys


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
    print collection.convert_collection_to_json()

if __name__ == '__main__':
    sys.exit(main())
