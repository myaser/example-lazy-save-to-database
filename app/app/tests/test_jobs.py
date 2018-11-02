from sqlalchemy import exists
from app.jobs import process_row
from app.tests.base import BaseTestCase
from app.schema import Users, session_scope


class TestJobs(BaseTestCase):

    def test_process_incorrect_row_size(self):
        self.assertEqual(process_row.queue(b'a,b,c').result,
                         {'success': False, 'message': 'row must contain 2 values separated by column `,`'})
        self.assertEqual(process_row.queue(b'abc').result,
                         {'success': False, 'message': 'row must contain 2 values separated by column `,`'})

    def test_process_invalid_email(self):
        self.assertEqual(process_row.queue(b'a,invalid_email_pattern').result,
                         {'success': False, 'message': 'email is not valid'})

    def test_success(self):
        self.assertEqual(process_row.queue(b'a,mail@example.com').result,
                         {'success': True})
        with session_scope() as session:
            self.assertTrue(session.query(exists().where(Users.email == 'mail@example.com')).scalar())

    def test_duplicated(self):
        self.assertEqual(process_row.queue(b'a,mail@example.com').result,
                         {'success': True})
        self.assertEqual(process_row.queue(b'a,mail@example.com').result,
                         {'success': False, 'message': 'email already exists'})
