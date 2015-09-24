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
        self.name = field_name
        self.type = field_type


class OdooRelation:

    def __init__(self, name, multiplicity, model):
        if not isinstance(name, str):
            raise TypeError('String expected, received %s' % type(name))
        if not isinstance(multiplicity, str):
            raise TypeError('String expected, received %s' % type(multiplicity))
        if not isinstance(model, str):
            raise TypeError('String expected, received %s' % type(model))
        self.name = name
        self.type = multiplicity
        self.model = model


class OdooClass:

    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError('String expected, received %s' % type(name))
        self.name = name
        self.fields = []
        self.relations = []

    def add_field(self, field):
        if not isinstance(field, OdooField):
            raise TypeError('OdooField expected, received %s' % type(field))
        self.fields.append(field)

    def add_relation(self, relation):
        if not isinstance(relation, OdooRelation):
            raise TypeError('OdooRelation expected, received %s' % type(relation))
        self.relations.append(relation)


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
relation_models = []

print 'Obtaining model list...'
models = client.models()
models = {models[key]._name: models[key] for key in models.keys()}

if args.f:
    models = {k: models[k] for k in models.keys() if args.f in k}

for model in models.keys():
    oclass = OdooClass(model)
    fields = models[model].fields()
    for f in fields.keys():
        field_type = fields[f]['type']
        if field_type == 'many2one' or field_type == 'many2many' or field_type == 'one2many':
            relation_model = fields[f]['relation']
            oclass.add_relation(OdooRelation(f, field_type, relation_model))
            if relation_model not in relation_models and relation_model not in models.keys():
                relation_models.append(relation_model)
        else:
            oclass.add_field(OdooField(f, field_type))
    classes.append(oclass)

for model in relation_models:
    oclass = OdooClass(model)
    classes.append(oclass)

print json.dumps(classes, cls=CustomEncoder)
