__author__ = 'joelortiz'

import erppeek
import argparse
import json
from json import JSONEncoder

SERVER_URL = 'http://localhost:8069'
DB_NAME = 'default_db'
USERNAME = 'admin'

parser = argparse.ArgumentParser(description='Quick JSON file generator containing model schema of the provided Odoo DB'
                                             ' - eg -d <dbname> -u <username>')
parser.add_argument('-s', help='URL of the Odoo server.')
parser.add_argument('-d', help='Name of the database to connect to.')
parser.add_argument('-u', help='Username to use when connecting to the database.')
parser.add_argument('-f', help='Filter to only get classes that contain this string.')

args = parser.parse_args()


class OdooField:

    def __init__(self, field_name, field_type):
        if not isinstance(field_name, str):
            raise TypeError('String expected, received %s' % type(field_name))
        if not isinstance(field_type, str):
            raise TypeError('String expected, received %s' % type(field_type))
        self.n = field_name
        self.t = field_type


class OdooClass:

    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError('String expected, received %s' % type(name))
        self.n = name
        self.fields = []
        self.relations = []

    def add_field(self, field):
        if not isinstance(field, OdooField):
            raise TypeError('Field expected, received %s' % type(field))
        self.fields.append(field)


class CustomEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

if args.s:
    SERVER_URL = args.s
if args.d:
    DB_NAME = args.d
if args.u:
    USERNAME = args.u

client = erppeek.Client(SERVER_URL, DB_NAME, USERNAME)
classes = []

print 'Obtaining model list...'
models = client.models()
models = {models[key]._name: models[key] for key in models.keys()}

if args.f:
    models = {k: models[k] for k in models.keys() if args.f in k}
print 'Model list obtained.'

for model in models.keys():
    oclass = OdooClass(model)
    fields = models[model].fields()
    [oclass.add_field(OdooField(f, fields[f]['type'])) for f in fields.keys()]
    classes.append(oclass)

print json.dumps(classes, cls=CustomEncoder)
