import erppeek
import json
from json import JSONEncoder


class OdooField:

    def __init__(self, field_name, field_type):
        if not isinstance(field_name, str):
            raise TypeError('String expected, received {0}'.format(
                type(field_name)))
        if not isinstance(field_type, str):
            raise TypeError('String expected, received {0}'.format(
                type(field_type)))
        self.name = field_name
        self.type = field_type


class OdooRelation:

    def __init__(self, name, multiplicity, model):
        if not isinstance(name, str):
            raise TypeError('String expected, received {0}'.format(
                type(name)))
        if not isinstance(multiplicity, str):
            raise TypeError('String expected, received {0}'.format(
                type(multiplicity)))
        if not isinstance(model, str):
            raise TypeError('String expected, received {0}'.format(
                type(model)))
        self.name = name
        self.type = multiplicity
        self.model = model


class OdooClass:

    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError('String expected, received {0}'.format(
                type(name)))
        self.name = name
        self.fields = []
        self.relations = []

    def add_field(self, field):
        if not isinstance(field, OdooField):
            raise TypeError('OdooField expected, received {0}'.format(
                type(field)))
        self.fields.append(field)

    def add_relation(self, relation):
        if not isinstance(relation, OdooRelation):
            raise TypeError('OdooRelation expected, received {0}'.format(
                type(relation)))
        self.relations.append(relation)


class CustomEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class OdooModelCollection:

    def __init__(self, model_filter=None, server='http://localhost:8069',
                 db='default_db',
                 user='admin',
                 password='admin'):
        try:
            self.client = erppeek.Client(server=server,
                                         db=db,
                                         user=user,
                                         password=password)
        except:
            raise RuntimeError('Error connecting to {0} on {1} '
                               'using credentials {2}:{3}'.format(db,
                                                                  server,
                                                                  user,
                                                                  password))
        self.classes = []
        self.relation_models = []
        self.model_filter = model_filter

    def convert_collection_to_json(self):
        print 'Obtaining model list...'
        models = self.client.models()
        models = {models[key]._name: models[key] for key in models.keys()}

        if self.model_filter:
            models = {k: models[k] for k in models.keys() if
                      self.model_filter in k}

        for model in models.keys():
            oclass = OdooClass(model)
            fields = models[model].fields()
            for f in fields.keys():
                field_type = fields[f]['type']
                if field_type == 'many2one' or field_type == 'many2many' or \
                        field_type == 'one2many':
                    relation_model = fields[f]['relation']
                    oclass.add_relation(OdooRelation(f,
                                                     field_type,
                                                     relation_model))
                    if relation_model not in self.relation_models and \
                            relation_model not in models.keys():
                        self.relation_models.append(relation_model)
                else:
                    oclass.add_field(OdooField(f, field_type))
            self.classes.append(oclass)

        for model in self.relation_models:
            oclass = OdooClass(model)
            self.classes.append(oclass)

        return json.dumps(self.classes, cls=CustomEncoder)
