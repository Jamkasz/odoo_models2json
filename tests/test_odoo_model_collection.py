__author__ = 'joelortiz'

import unittest
from mock import MagicMock
from mock import patch
from odoo_models.odoo_model_collection import OdooModelCollection


class TestOdooClass(unittest.TestCase):

    @patch('erppeek.Client')
    def test_01_init(self, mock_client):
        """
        Test initializing an OdooModelCollection starts a connection with an Odoo server using ERPPeek and
        initializes the parameters correctly.
        :param mock_client: A mocked out version of erppeek.Client
        :return:
        """
        test_omc = OdooModelCollection()
        self.assertIsInstance(test_omc.client, MagicMock)
        self.assertListEqual(test_omc.classes, [])
        self.assertListEqual(test_omc.relation_models, [])
        self.assertFalse(test_omc.model_filter)
        mock_client.stop()

    def test_02_init_throws_runtime_exception_when_connection_fails(self):
        """
        Test initializing an OdooModelCollection throws a RuntimeError when failing to connect to the server.
        :return:
        """
        with self.assertRaises(RuntimeError):
            OdooModelCollection()

    @patch('erppeek.Client')
    def test_03_get_classes(self, mock_client):
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
    def test_04_get_relation_models(self, mock_client):
        """
        Test that get_relation_models returns the relation_models parameter of the OdooModelCollection object.
        :param mock_client: A mocked out version of erppeek.Client
        :return:
        """
        test_omc = OdooModelCollection()
        test_omc.relation_models = ['model']
        self.assertListEqual(['model'], test_omc.get_relation_models())
        mock_client.stop()
