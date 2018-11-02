from functools import partial
import os
from contextlib import contextmanager

from sqlalchemy import (Column, String)
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

create_engine = partial(create_engine, echo=True, convert_unicode=True,
                        pool_size=200, pool_recycle=170, isolation_level="READ COMMITTED")

engine = create_engine(os.environ['DATABASE_URL'])
Session = sessionmaker(bind=engine, autoflush=False)


class Base(object):
    """
    a base class for all of our models, this defines:
    1) the table name to be the lower-cased version of the class name
    2) generic __init__ and __repr__ functions
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __init__(self, **kwargs):
        for key in kwargs:
            if key not in self.attr_accessor:
                raise Exception(f'Invalid Prop: {key}')
            setattr(self, key, kwargs[key])

    def to_dict(self):
        return {
            k: v for k, v in self.__dict__.items() if not k.startswith('_')
        }

    def __repr__(self):
        def filter_properties(obj):
            # this function decides which properties should be exposed through repr
            properties = obj.__dict__.keys()
            for prop in properties:
                if prop[0] != "_" and not callable(prop):
                    yield (prop, str(getattr(obj, prop)))
            return

        prop_tuples = filter_properties(self)
        prop_string_tuples = (": ".join(prop) for prop in prop_tuples)
        prop_output_string = " | ".join(prop_string_tuples)
        cls_name = self.__module__ + "." + self.__class__.__name__

        return "<%s('%s')>" % (cls_name, prop_output_string)


Base = declarative_base(cls=Base)


class Users(Base):
    email = Column(String, primary_key=True)
    name = Column(String)


@contextmanager
def session_scope(session_maker=Session):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


target_metadata = Base.metadata
