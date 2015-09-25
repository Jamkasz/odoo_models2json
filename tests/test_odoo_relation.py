__author__ = 'joelortiz'

import unittest
from odoo_models.odoo_model_collection import OdooRelation


class TestOdooRelation(unittest.TestCase):

    def test_01_init(self):
        """
        Test that when initializing an OdooRelation the name, type and model parameters are set correctly.
        :return:
        """
        test_or = OdooRelation('name', 'type', 'model')
        self.assertEqual(test_or.name, 'name', 'Name set by init is not correct')
        self.assertEqual(test_or.type, 'type', 'Type set by init is not correct')
        self.assertEqual(test_or.model, 'model', 'Model set by init is not correct')

    def test_02_init_throws_unexpected_type_exception_with_non_string_name(self):
        """
        Test that when initializing an OdooRelation with a non string name parameter, a TypeError exception is thrown.
        :return:
        """
        names = [True, 1, 1.5, ['name'], {'name': 'name'}, {'name'}]
        for name in names:
            with self.assertRaises(TypeError):
                OdooRelation(name, 'type', 'model')

    def test_03_init_throws_unexpected_type_exception_with_non_string_type(self):
        """
        Test that when initializing an OdooRelation with a non string type parameter, a TypeError exception is thrown.
        :return:
        """
        types = [True, 1, 1.5, ['type'], {'type': 'type'}, {'type'}]
        for t in types:
            with self.assertRaises(TypeError):
                OdooRelation('name', t, 'model')
    
    def test_04_init_throws_unexpected_type_exception_with_non_string_model(self):
        """
        Test that when initializing an OdooRelation with a non string model parameter, a TypeError exception is thrown.
        :return:
        """
        models = [True, 1, 1.5, ['model'], {'model': 'model'}, {'model'}]
        for model in models:
            with self.assertRaises(TypeError):
                OdooRelation('name', 'type', model)

    def test_05_get_name(self):
        """
        Test that get_name returns the name parameter of the OdooRelation object
        :return:
        """
        test_or = OdooRelation('name', 'type', 'model')
        self.assertEqual('name', test_or.get_name())

    def test_06_get_type(self):
        """
        Test that get_type returns the type parameter of the OdooRelation object
        :return:
        """
        test_or = OdooRelation('name', 'type', 'model')
        self.assertEqual('type', test_or.get_type())

    def test_07_get_model(self):
        """
        Test that get_model returns the model parameter of the OdooRelation object
        :return:
        """
        test_or = OdooRelation('name', 'type', 'model')
        self.assertEqual('model', test_or.get_model())
