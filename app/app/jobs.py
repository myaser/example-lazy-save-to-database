from flask_rq2 import RQ
from sqlalchemy.exc import IntegrityError
from validate_email import validate_email
from tempfile import SpooledTemporaryFile

rq = RQ()


@rq.job
def process_row(row: bytes) -> dict:
    from .schema import Users, session_scope
    try:
        row = row.decode("utf-8")
        name, email = row.split(',')
        if not validate_email(email):
            return {'success': False, 'message': 'email is not valid'}
        with session_scope() as session:
            session.add(Users(email=email, name=name))
    except ValueError as e:
        return {'success': False, 'message': 'row must contain 2 values separated by column `,`'}
    except IntegrityError as e:
        return {'success': False, 'message': 'email already exists'}
    else:
        return {'success': True}


@rq.job
def process_file(file: SpooledTemporaryFile):
    for line in file:
        process_row.queue(line.strip())