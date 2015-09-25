""" Tests for HTML Output:
 - On receiving an empty Odoo Collection it raises an error
 - On receiving a valid Odoo Collection it converts this to JSON and renders the
    template to the output directory
 - It raises and error if the output directory is not valid
"""
import unittest
from mock import Mock, MagicMock
from odoo_models.odoo_model_collection import OdooModelCollection, OdooClass, OdooField
from odoo_models.html_formatter import HTMLFormatter
from jinja2 import Environment, Template

class TestHtmlOutput(unittest.TestCase):
    """ HTML Output tests
    """

    def setUp(self):
        # Set up demo objects
        field1 = OdooField('name', 'char')
        field2 = OdooField('dob', 'datetime')
        field3 = OdooField('location', 'char')
        class1 = OdooClass('test.class.one')
        class1.add_field(field1)
        class1.add_field(field2)
        class1.add_field(field3)
        class2 = OdooClass('test.class.two')
        class2.add_field(field1)
        class2.add_field(field2)
        self.mock_json = '[{"fields": [{"name": "name", "type": "char"}' \
                         '{"name": "dob", "type": "datetime"}' \
                         '{"name": "location", "type": "char"}], ' \
                         '"name": "test.class.one", "relations":[]},{' \
                         '"fields": [{"name": "name", "type": "char"}' \
                         '{"name": "dob", "type": "datetime"}], ' \
                         '"name": "test.class.two", ' \
                         '"relations": []}]'
        self.valid_collection = Mock(spec=OdooModelCollection)
        self.valid_collection.get_classes = MagicMock(return_value=[class1,
                                                                    class2])
        self.invalid_collection = []
        self.empty_collection = Mock(spec=OdooModelCollection)
        self.empty_collection.get_classes = MagicMock(return_value=[])

    def test_01_raises_on_empty_collection(self):
        with self.assertRaises(ValueError):
            html = HTMLFormatter(collection=self.empty_collection)

    def test_02_raises_on_invalid_collection(self):
        with self.assertRaises(ValueError):
            html = HTMLFormatter(collection=self.invalid_collection)

    def test_03_calls_render_html_on_valid_collection(self):
        mock_html_formatter = HTMLFormatter
        orig_render_html = mock_html_formatter.render_html

        mock_html_formatter.render_html = MagicMock()
        html = HTMLFormatter(collection=self.valid_collection)
        mock_html_formatter.render_html.assert_called_once_with()

        mock_html_formatter.render_html.stop()
        mock_html_formatter.render_html = orig_render_html

    def test_04_converts_collection_to_json_in_order_to_render_html(self):
        # mock out JSON
        mock_collection = self.valid_collection
        orig_json_func = mock_collection.convert_collection_to_json
        mock_collection.convert_collection_to_json = MagicMock(
            return_value=self.mock_json)

        # mock out jinja2
        mock_env = Environment
        orig_get_template = mock_env.get_template
        mock_env.get_template = MagicMock(
            return_value=Template('<html><script>var graph = '
                                  '{{ collection_json }};</script></html>'))
        mock_html = '<html><script>var graph = {0};</script></html>'.format(
            self.mock_json
        )

        html = HTMLFormatter(collection=self.valid_collection)
        mock_collection.convert_collection_to_json.assert_called_once_with()
        print html.html
        self.assertEqual(mock_html, html.html, 'HTML outputs not equal')

        mock_env.get_template.stop()
        mock_env.get_template = orig_get_template
        mock_collection.convert_collection_to_json.stop()
        mock_collection.convert_collection_to_json = orig_json_func


