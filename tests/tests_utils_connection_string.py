# coding: utf8
import unittest
from os.path import abspath
from dbaggregator.utils import DBAggregatorException
from dbaggregator.utils.connection_string import (
    conn_str_by_dict,
    conn_str_by_iniconf,
)


class TestUtilsConnectionString(unittest.TestCase):

    def setUp(self):
        self.dbconf_mysql = {
            'dialect': 'mysql',
            'user': 'usr',
            'password': '123change',
            'host': '127.0.0.1',
            'port': '3306',
            'db': 'localdb',
        }

        self.dbconf_psql = {
            'dialect': 'postgresql',
            'driver': 'psycopg2',
            'user': 'usr',
            'password': '123change',
            'host': '127.0.0.1',
            'port': '5432',
            'db': 'localdb',
        }

        self.iniconf_path = abspath('tests/iniconf_test.ini')

    def test_conn_str_by_dict_requireds(self):
        db_conf = self.dbconf_mysql.copy()
        db_conf.pop('dialect')
        with self.assertRaises(DBAggregatorException) as cm:
            conn_str_by_dict(db_conf)
        self.assertIn('"dialect"', str(cm.exception))


        db_conf = self.dbconf_mysql.copy()
        db_conf['dialect'] = 'sqlite'
        with self.assertRaises(DBAggregatorException) as cm:
            conn_str_by_dict(db_conf)
        self.assertIn('"sqlite"', str(cm.exception))


        db_conf = self.dbconf_mysql.copy()
        db_conf.pop('user')
        with self.assertRaises(DBAggregatorException) as cm:
            conn_str_by_dict(db_conf)
        self.assertIn('"user"', str(cm.exception))


        db_conf = self.dbconf_mysql.copy()
        db_conf.pop('password')
        with self.assertRaises(DBAggregatorException) as cm:
            conn_str_by_dict(db_conf)
        self.assertIn('"password"', str(cm.exception))


        db_conf = self.dbconf_mysql.copy()
        db_conf.pop('host')
        with self.assertRaises(DBAggregatorException) as cm:
            conn_str_by_dict(db_conf)
        self.assertIn('"host"', str(cm.exception))


        db_conf = self.dbconf_mysql.copy()
        db_conf.pop('port')
        with self.assertRaises(DBAggregatorException) as cm:
            conn_str_by_dict(db_conf)
        self.assertIn('"port"', str(cm.exception))


        db_conf = self.dbconf_mysql.copy()
        db_conf.pop('db')
        with self.assertRaises(DBAggregatorException) as cm:
            conn_str_by_dict(db_conf)
        self.assertIn('"db"', str(cm.exception))


    def test_conn_str_by_dict_psql(self):
        self.assertEqual(
            'postgresql+psycopg2://usr:123change@127.0.0.1:5432/localdb',
            conn_str_by_dict(self.dbconf_psql)
        )

    def test_conn_str_by_dict_mysql(self):
        self.assertEqual(
            'mysql://usr:123change@127.0.0.1:3306/localdb',
            conn_str_by_dict(self.dbconf_mysql)
        )

    def test_conn_str_by_iniconf(self):
        result = conn_str_by_iniconf(self.iniconf_path, ['db-mysql', 'db-psql'])

        self.assertTrue(isinstance(result, dict))
        self.assertEqual(2, len(result))
        self.assertIn('db-mysql', result)
        self.assertIn('db-psql', result)

        self.assertEqual(
            'postgresql+psycopg2://usr:123change@127.0.0.1:5432/localdb',
            result['db-psql']
        )
        self.assertEqual(
            'mysql://usr:123change@127.0.0.1:3306/localdb',
            result['db-mysql']
        )


if __name__ == '__main__':
    unittest.main()
