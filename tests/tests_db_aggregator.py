# coding: utf8
import unittest
from db_aggregator.db_aggregator import DBAggregator


db_conn = 'sqlite:///tests/foo.db'


class TestDBAggregator(unittest.TestCase):

    def setUp(self):
        self.db_conn = getattr(self, 'db_conn', db_conn)

        db = DBAggregator()
        db.add('db1', self.db_conn)
        conn = db.db1.engine.connect()

        if hasattr(db.db1.tables, 'TbX'):
            conn.execute('DROP TABLE tb_x')

        conn.execute('CREATE TABLE tb_x (a INTEGER PRIMARY KEY, b INTEGER)')
        conn.execute('INSERT INTO tb_x (a, b) VALUES (1, 10)')
        conn.execute('INSERT INTO tb_x (a, b) VALUES (2, 20)')

        db.add('db_test', self.db_conn)
        setattr(self, 'db_test', db.db_test)

    def test_attrs(self):
        db = DBAggregator()
        self.assertFalse(hasattr(db, 'my_db'))

        db.add('my_db', self.db_conn)
        self.assertTrue(hasattr(db, 'my_db'))

        self.assertTrue(hasattr(db.my_db, 'engine'))

        self.assertTrue(hasattr(db.my_db, 'sigle_session'))
        self.assertTrue(callable(db.my_db.sigle_session))

        self.assertTrue(hasattr(db.my_db, 'session'))
        self.assertTrue(callable(db.my_db.session))


        self.assertTrue(hasattr(db.my_db, 'tables'))

        self.assertTrue(hasattr(db.my_db, 'load_tables'))
        self.assertTrue(callable(db.my_db.load_tables))

        self.assertTrue(hasattr(db.my_db, 'set_new_table'))
        self.assertTrue(callable(db.my_db.set_new_table))

        self.assertTrue(hasattr(db.my_db, 'cursor'))
        self.assertTrue(callable(db.my_db.cursor))

    def test_load_table(self):
        self.db_conn = db_conn

        db = DBAggregator()
        db.add('db1', self.db_conn)
        conn = db.db1.engine.connect()

        if hasattr(db.db1.tables, 'TbY'):
            conn.execute('DROP TABLE tb_y')
        conn.execute('CREATE TABLE tb_y (a INTEGER PRIMARY KEY, b INTEGER)')

        if hasattr(db.db1.tables, 'TbZ'):
            conn.execute('DROP TABLE tb_z')
        conn.execute('CREATE TABLE tb_z (a INTEGER PRIMARY KEY, b INTEGER)')

        db.add('db2', self.db_conn)
        self.assertTrue(hasattr(db.db2.tables, 'TbX'))
        self.assertTrue(hasattr(db.db2.tables, 'TbY'))
        self.assertTrue(hasattr(db.db2.tables, 'TbZ'))

        db.add('db3', self.db_conn)
        db.db3.load_tables(['tb_x', 'tb_y'])
        self.assertTrue(hasattr(db.db3.tables, 'TbX'))
        self.assertTrue(hasattr(db.db3.tables, 'TbY'))
        self.assertFalse(hasattr(db.db3.tables, 'TbZ'))

    def test_session_filter(self):
        tbl = self.db_test.tables
        sess = self.db_test.session()

        q = sess.query(tbl.TbX)
        self.assertEqual(2, q.count())

        row1 = q.filter(tbl.TbX.a == 1).first()
        self.assertNotEqual(None, row1)
        self.assertEqual((1, 10), (row1.a, row1.b))
        self.assertTrue(isinstance(row1, tbl.TbX))

        row2 = q.filter(tbl.TbX.a == 2).first()
        self.assertNotEqual(None, row2)
        self.assertEqual((2, 20), (row2.a, row2.b))
        self.assertTrue(isinstance(row2, tbl.TbX))

    def test_session_insert(self):
        tbl = self.db_test.tables
        sess = self.db_test.session()

        row = tbl.TbX()
        row.a = 3
        row.b = 30
        sess.add(row)
        sess.commit()

        db = DBAggregator()
        db.add('db2', self.db_conn)

        tbl2 = db.db2.tables
        sess2 = db.db2.session()

        q = sess2.query(tbl2.TbX)
        q = q.filter(tbl2.TbX.a == 3)
        q = q.filter(tbl2.TbX.b == 30)
        self.assertEqual(1, q.count())

    def test_session_execute(self):
        import sqlalchemy as sa
        sess = self.db_test.session()


        r1 = sess.execute(sa.sql.text(u'''
            SELECT
                COUNT(1) AS count
            FROM tb_x
        '''))

        row1 = r1.fetchone()
        self.assertNotEqual(None, row1)
        self.assertEqual(2, row1.count)


        q2 = sa.sql.text(u'''
            SELECT
                a,
                b
            FROM tb_x
            WHERE
                a = :p_a
                AND b = :p_b
        ''')
        r2 = sess.execute(q2, params={'p_a': 1, 'p_b': 10})

        row2 = r2.fetchone()
        self.assertNotEqual(None, row2)
        self.assertTrue(hasattr(row2, 'a'))
        self.assertTrue(hasattr(row2, 'b'))

        self.assertEqual(None, r2.fetchone())


if __name__ == '__main__':
    unittest.main()
