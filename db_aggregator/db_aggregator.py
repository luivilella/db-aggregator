# coding: utf8
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


def snake2camel(value):
    return ''.join([x.capitalize() for x in value.split('_')])


class LoadTables(object):

    def __init__(self, engine, tables=None):
        self.engine = engine
        self.Base = declarative_base(bind=self.engine)
        self.tables = tables or sa.inspect(self.engine).get_table_names()
        self._load_tables()

    def _load_tables(self):
        for tablename in self.tables:
            tablename = str(tablename)
            table_class_name = snake2camel(tablename)

            setattr(
                self,
                table_class_name,
                type(table_class_name, (self.Base,), {
                    '__tablename__': tablename,
                    '__table_args__': {'autoload': True},
                })
            )

class DB(object):

    def __init__(self, engine):
        super(DB, self).__init__()
        self.engine = engine
        self.sigle_session = sa.orm.sessionmaker(bind=self.engine)
        self.session = sa.orm.scoped_session(sa.orm.sessionmaker(bind=self.engine))
        self._tables = None
        self._tables_to_load = None

    def cursor(self):
        return self.engine.raw_connection().cursor()

    def load_tables(self, tables):
        self._tables_to_load = tables

    def set_new_table(self, name, obj):
        setattr(self.tables, name, obj)

    @property
    def tables(self):
        if self._tables is None:
            self._tables = LoadTables(self.engine, tables=self._tables_to_load)

        return self._tables


class DBAggregator(object):

    def add(self, db_name, conn_string, engine_args=None):
        engine_args = engine_args or {}
        engine = sa.create_engine(conn_string, **engine_args)
        setattr(self, db_name, DB(engine))
