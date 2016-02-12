# dbaggregator
==============

Package helpful to manage database connections

## Instalation

    pip install git+https://github.com/luivilella/dbaggregator.git

## Basic Usage

    from dbaggregator import DBAggregator

    db = DBAggregator()

    db.add('psql', 'postgresql+psycopg2://usr:123change@127.0.0.1:5432/localdb')
    db.add('mysql', 'mysql://usr:123change@127.0.0.1:3306/localdb')
    db.add('sqlite', ''sqlite:///tests/foo.db'')

    sess = db.psql.session()
    tbls = db.psql.tables

    #find
    row = sess.query(tbls.TableA).filter(tbls.TableA.id == 1).first()

    #insert
    obj = TableA()
    obj.name = 'test'

    sess.add(obj)
    sess.commit()

    #sql
    sess.execute('SELECT * FROM table_a')
