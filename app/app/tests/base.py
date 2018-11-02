import contextlib
from flask_testing import TestCase
from app.schema import engine, target_metadata
from app import create_app

app = create_app()


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        pass

    def tearDown(self):
        with contextlib.closing(engine.connect()) as con:
            trans = con.begin()
            for table in reversed(target_metadata.sorted_tables):
                con.execute(table.delete())
            trans.commit()
