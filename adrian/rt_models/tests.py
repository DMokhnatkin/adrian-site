import os

from django.test import TestCase, override_settings
from . import models
from django.conf import settings
from django.db.models import Model, DecimalField
from django.db import connection

from .models import reg_model_python, reg_model_attrs, get_sourcecode_path


class TestRtModel1(Model):
    from django.db.models import IntegerField
    test_field_1 = IntegerField()


class ModelsTestCase(TestCase):
    @override_settings(RT_MODELS_PATH='test_rt_models.py')
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @override_settings(RT_MODELS_PATH='test_rt_models.py')
    def test_sourcecode_creation_from_python(self):
        """
        Test if reg_model_from_python creates file with source code
        """
        try:
            reg_model_python(TestRtModel1, False)
            self.assertTrue(
                os.path.isfile(
                    os.path.join(
                        os.path.dirname(__file__),
                        'test_rt_models.py')
                )
            )
        finally:
            if os.path.exists(get_sourcecode_path('rt_models')):
                os.remove(get_sourcecode_path('rt_models'))
            pass

    @override_settings(RT_MODELS_PATH='test_rt_models.py')
    def test_sourcecode_creation_from_attrs(self):
        """
        Test if reg_model_from_attrs creates file with source code
        """
        try:
            reg_model_attrs(
                'TestRtModel2',
                'rt_models',
                {'test_field_1': DecimalField}
            )
            self.assertTrue(
                os.path.isfile(
                    os.path.join(
                        os.path.dirname(__file__),
                        'test_rt_models.py')
                )
            )
        finally:
            if os.path.exists(get_sourcecode_path('rt_models')):
                os.remove(get_sourcecode_path('rt_models'))
            pass

