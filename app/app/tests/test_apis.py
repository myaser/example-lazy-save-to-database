from io import BytesIO
import simplejson as json
from sqlalchemy import exists

from app.tests.base import BaseTestCase
from app.schema import Users, session_scope


class TestAPIBlueprint(BaseTestCase):

    def test_bad_request(self):
        payload = {}
        response = self.client.post(
            '/api/upload/',
            content_type='multipart/form-data', data=payload
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual('No file part', data['message'])

        payload = {
            'file': (BytesIO(b'my file contents'), "file.ext"),
        }
        response = self.client.post(
            '/api/upload/',
            content_type='multipart/form-data', data=payload
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual('un supported file type', data['message'])

    def test_csv_file(self):
        payload = {
            'file': (BytesIO(b'my file contents'), "file.csv"),
        }
        response = self.client.post(
            '/api/upload/',
            content_type='multipart/form-data', data=payload
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual('we are processing your file', data['message'])

    def test_data_were_saved(self):
        payload = {
            'file': (BytesIO(
                b"""name,mail@example.com
                name2,mail@example.com
                name
                name,email
                """
            ), "file.csv"),
        }
        response = self.client.post(
            '/api/upload/',
            content_type='multipart/form-data', data=payload
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual('we are processing your file', data['message'])
        with session_scope() as session:
            self.assertEqual(session.query(Users).count(), 1)
            self.assertTrue(session.query(exists().where(Users.email == 'mail@example.com')).scalar())
            self.assertEqual(session.query(Users).get('mail@example.com').name, 'name')
