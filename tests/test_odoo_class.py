__author__ = 'joelortiz'

import unittest
from odoo_models.odoo_model_collection import OdooClass, OdooField, OdooRelation


class TestOdooClass(unittest.TestCase):

    def test_01_init(self):
        """
        Test that when initializing an OdooClass the parameters are set correctly.
        :return:
        """
        test_oc = OdooClass('name')
        self.assertEqual(test_oc.name, 'name', 'Name set by init is not correct')
        self.assertListEqual(test_oc.fields, [], 'Fields set by init is not correct')
        self.assertListEqual(test_oc.relations, [], 'Relations set by init is not correct')

    def test_02_init_throws_unexpected_type_exception_with_non_string_name(self):
        """
        Test that when initializing an OdooClass with a non string name parameter, a TypeError exception is thrown.
        :return:
        """
        names = [True, 1, 1.5, ['name'], {'name': 'name'}, {'name'}]
        for name in names:
            with self.assertRaises(TypeError):
                OdooClass(name)

    def test_03_get_name(self):
        """
        Test that get_name returns the name parameter of the OdooClass object
        :return:
        """
        test_oc = OdooClass('name')
        self.assertEqual('name', test_oc.get_name())

    def test_04_get_fields(self):
        """
        Test that get_fields returns the fields parameter of the OdooClass object
        :return:
        """
        test_oc = OdooClass('name')
        test_oc.fields = ['field']
        self.assertListEqual(['field'], test_oc.get_fields())

    def test_05_get_relations(self):
        """
        Test that get_relations returns the relations parameter of the OdooClass object
        :return:
        """
        test_oc = OdooClass('name')
        test_oc.relations = ['relation']
        self.assertListEqual(['relation'], test_oc.get_relations())

    def test_06_add_field(self):
        """
        Test that OdooField objects are added correctly using add_field method
        :return:
        """
        test_oc = OdooClass('name')
        test_oc.add_field('field', 'type')
        fields = test_oc.get_fields()
        self.assertEqual(len(fields), 1)
        self.assertIsInstance(fields[0], OdooField)

    def test_07_add_relation(self):
        """
        Test that OdooRelation objects are added correctly using add_relation method
        :return:
        """
        test_oc = OdooClass('name')
        test_oc.add_relation('name', 'type', 'model')
        relations = test_oc.get_relations()
        self.assertEqual(len(relations), 1)
        self.assertIsInstance(relations[0], OdooRelation)
