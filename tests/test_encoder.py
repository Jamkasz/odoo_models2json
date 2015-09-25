__author__ = 'joelortiz'

import unittest
import json
from odoo_models.odoo_model_collection import CustomEncoder, OdooClass


class TestCustomEncoder(unittest.TestCase):

    def test_01_default(self):
        """
        Test that when encoding an object the encoder returns the underlying dictionary by default.
        :return:
        """
        test_oc = OdooClass('name')
        dictionary = test_oc.__dict__
        result = json.dumps(test_oc, cls=CustomEncoder)
        self.assertDictEqual(eval(result), dictionary)
