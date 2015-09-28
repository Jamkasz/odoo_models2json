# pylint: disable=maybe-no-member,too-few-public-methods
""" Formatter to provide HTML output for an Odoo Model Collection
"""
from odoo_model_collection import OdooModelCollection
from jinja2 import Environment, FileSystemLoader
import os

class HTMLFormatter(object):
    """ A class for handling the HTML output functionality
    """

    def __init__(self, collection=None):
        if isinstance(collection, OdooModelCollection):
            if len(collection.get_classes()) > 0:
                self.collection = collection
                self.html = self.render_html()
            else:
                raise ValueError('OdooModelCollection passed is empty')
        else:
            raise ValueError('Invalid object passed, should be instance of'
                             'OdooModelCollection')

    def render_html(self):
        """ Method to turn an OdooModelCollection into a HTML Page
        :return: A string of HTML
        """
        collection_json = self.collection.convert_collection_to_json()
        env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
        template = env.get_template('curved_links.html')
        return template.render(collection_json=collection_json)
