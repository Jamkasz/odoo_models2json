import unittest
# from odoo_models import odoo_model_collection
from odoo_models import OdooField


class TestOdooField(unittest.TestCase):

    def test_01_init(self):
        """
        Test that when initializing an OdooField the name and type parameters are set correctly.
        :return:
        """
        test_of = OdooField('name', 'type')
        self.assertEqual(test_of.name, 'name', 'Name set by init is not correct')
        self.assertEqual(test_of.type, 'type', 'Type set by init is not correct')

    def test_02_init_throws_unexpected_type_exception_with_non_string_name(self):
        """
        Test that when initializing an OdooField with a non string name parameter, a TypeError exception is thrown.
        :return:
        """
        names = [True, 1, 1.5, ['name'], {'name': 'name'}, {'name'}]
        for name in names:
            self.assertRaises(TypeError, OdooField(name, 'type'))

    def test_03_init_throws_unexpected_type_exception_with_non_string_type(self):
        """
        Test that when initializing an OdooField with a non string type parameter, a TypeError exception is thrown.
        :return:
        """
        types = [True, 1, 1.5, ['type'], {'type': 'type'}, {'type'}]
        for t in types:
            self.assertRaises(TypeError, OdooField('name', t))

    def test_04_get_name(self):
        """
        Test that get_name returns the name parameter of the OdooField object
        :return:
        """
        test_of = OdooField('name', 'type')
        self.assertEqual('name', test_of.get_name())

    def test_05_get_type(self):
        """
        Test that get_type returns the type parameter of the OdooField object
        :return:
        """
        test_of = OdooField('name', 'type')
        self.assertEqual('type', test_of.get_type())
