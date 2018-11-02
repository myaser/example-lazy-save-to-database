# project/tests/test_config.py


import unittest

from flask import current_app
from flask_testing import TestCase

from app import create_app


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        return create_app(app_settings='app.config.DevelopmentConfig')

    def test_app_is_development(self):
        self.assertTrue(self.app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(self.app.config['RQ_ASYNC'])


class TestTestingConfig(TestCase):
    def create_app(self):
        return create_app(app_settings='app.config.TestingConfig')

    def test_app_is_testing(self):
        # self.assertEqual(self.app.config['RQ_CONNECTION_CLASS'], 'fakeredis.FakeStrictRedis')
        self.assertFalse(self.app.config['RQ_ASYNC'])
        self.assertTrue(self.app.config['DEBUG'])
        self.assertTrue(self.app.config['TESTING'])


class TestProductionConfig(TestCase):
    def create_app(self):
        return create_app(app_settings='app.config.ProductionConfig')

    def test_app_is_production(self):
        self.assertFalse(self.app.config['DEBUG'])
        self.assertFalse(self.app.config['TESTING'])
        self.assertTrue(self.app.config['RQ_ASYNC'])


if __name__ == '__main__':
    unittest.main()
