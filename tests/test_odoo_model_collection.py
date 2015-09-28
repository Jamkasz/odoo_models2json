__author__ = 'joelortiz'

import unittest
from mock import MagicMock
from mock import patch
from odoo_models.odoo_model_collection import OdooModelCollection, OdooClass
import erppeek


class TestOdooClass(unittest.TestCase):

    def test_01_init(self):
        """
        Test initializing an OdooModelCollection starts a connection with an Odoo server using ERPPeek and
        initializes the parameters correctly.
        :return:
        """
        # Mock Up
        mock_client = MagicMock()
        model_1 = MagicMock()
        model_1._name = 'test.model.1'
        model_1.fields = MagicMock(return_value={
            'm1_f1': {'type': 'boolean'},
            'm1_f2': {'type': 'char'},
            'm1_f3': {'type': 'many2one', 'relation': 'test.model.2'},
        })
        model_2 = MagicMock()
        model_2._name = 'test.model.2'
        model_2.fields = MagicMock(return_value={
            'm2_f1': {'type': 'text'},
            'm2_f2': {'type': 'many2many', 'relation': 'test.model.3'},
            'm2_f3': {'type': 'one2many', 'relation': 'test.model.1'},
        })
        mock_client.models = MagicMock(return_value={'Model 1': model_1, 'Model 2': model_2})
        mock_erppeek = MagicMock(return_value=mock_client)

        with patch('erppeek.Client', mock_erppeek):
            test_omc = OdooModelCollection()
            self.assertIsInstance(test_omc.client, MagicMock)
            self.assertEqual(len(test_omc.classes), 3)
            self.assertIsInstance(test_omc.classes[0], OdooClass)
            self.assertIsInstance(test_omc.classes[1], OdooClass)
            self.assertIsInstance(test_omc.classes[2], OdooClass)
            self.assertEqual(len(test_omc.relation_models), 1)
            self.assertEqual(test_omc.relation_models[0], 'test.model.3')
            self.assertFalse(test_omc.model_filter)

    def test_02_init_throws_runtime_exception_when_connection_fails(self):
        """
        Test initializing an OdooModelCollection throws a RuntimeError when failing to connect to the server.
        :return:
        """
        with self.assertRaises(RuntimeError):
            OdooModelCollection()

    def test_03_init_with_model_filter(self):
        """
        Test initializing an OdooModelCollection using a model_filter will not include models not matching the filter
        in the collection.
        :return:
        """
        # Mock Up
        mock_client = MagicMock()
        model_1 = MagicMock()
        model_1._name = 'test.model.1'
        model_1.fields = MagicMock(return_value={
            'm1_f1': {'type': 'boolean'},
            'm1_f2': {'type': 'char'},
            'm1_f3': {'type': 'many2one', 'relation': 'testing.model.2'},
        })
        model_2 = MagicMock()
        model_2._name = 'testing.model.2'
        model_2.fields = MagicMock(return_value={
            'm2_f1': {'type': 'text'},
            'm2_f2': {'type': 'many2many', 'relation': 'test.model.3'},
            'm2_f3': {'type': 'one2many', 'relation': 'test.model.1'},
        })
        mock_client.models = MagicMock(return_value={'Model 1': model_1, 'Model 2': model_2})
        mock_erppeek = MagicMock(return_value=mock_client)

        with patch('erppeek.Client', mock_erppeek):
            test_omc = OdooModelCollection('test.model')
            self.assertEqual(len(test_omc.classes), 2)
            self.assertIsInstance(test_omc.classes[0], OdooClass)
            self.assertIsInstance(test_omc.classes[1], OdooClass)
            self.assertEqual(len(test_omc.relation_models), 1)
            self.assertEqual(test_omc.relation_models[0], 'testing.model.2')
            self.assertEqual(test_omc.model_filter, 'test.model')

    @patch('erppeek.Client')
    def test_04_get_classes(self, mock_client):
        """
        Test that get_classes returns the classes parameter of the OdooModelCollection object.
        :param mock_client: A mocked out version of erppeek.Client
        :return:
        """
        test_omc = OdooModelCollection()
        test_omc.classes = ['class']
        self.assertListEqual(['class'], test_omc.get_classes())
        mock_client.stop()

    @patch('erppeek.Client')
    def test_05_get_relation_models(self, mock_client):
        """
        Test that get_relation_models returns the relation_models parameter of the OdooModelCollection object.
        :param mock_client: A mocked out version of erppeek.Client
        :return:
        """
        test_omc = OdooModelCollection()
        test_omc.relation_models = ['model']
        self.assertListEqual(['model'], test_omc.get_relation_models())
        mock_client.stop()

    def test_06_convert_collection_to_json(self):
        """
        Test json conversion is returned correctly.
        :return:
        """
        # Mock Up
        mock_client = MagicMock()
        model_1 = MagicMock()
        model_1._name = 'test.model.1'
        model_1.fields = MagicMock(return_value={
            'm1_f1': {'type': 'boolean'},
            'm1_f2': {'type': 'char'},
            'm1_f3': {'type': 'many2one', 'relation': 'test.model.2'},
        })
        model_2 = MagicMock()
        model_2._name = 'test.model.2'
        model_2.fields = MagicMock(return_value={
            'm2_f1': {'type': 'text'},
            'm2_f2': {'type': 'many2many', 'relation': 'test.model.3'},
            'm2_f3': {'type': 'one2many', 'relation': 'test.model.1'},
        })
        mock_client.models = MagicMock(return_value={'Model 1': model_1, 'Model 2': model_2})
        mock_erppeek = MagicMock(return_value=mock_client)

        with patch('erppeek.Client', mock_erppeek):
            test_omc = OdooModelCollection()
            json = [
                {
                    "fields": [{"type": "text", "name": "m2_f1"}],
                    "name": "test.model.2",
                    "relations": [
                        {"model": "test.model.1", "type": "one2many", "name": "m2_f3"},
                        {"model": "test.model.3", "type": "many2many", "name": "m2_f2"}
                    ]
                }, {
                    "fields": [{"type": "char", "name": "m1_f2"}, {"type": "boolean", "name": "m1_f1"}],
                    "name": "test.model.1",
                    "relations": [
                        {"model": "test.model.2", "type": "many2one", "name": "m1_f3"}
                    ]
                }, {
                    "fields": [],
                    "name": "test.model.3",
                    "relations": []
                }]
            self.assertListEqual(eval(test_omc.convert_collection_to_json()), json)
