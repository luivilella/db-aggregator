# coding: utf8
from ConfigParser import SafeConfigParser
from dbaggregator.utils import DBAggregatorException
from dbaggregator.dbaggregator import DBAggregator


def conn_str_by_dict(db_conf):
    required_params = (
        ('dialect', True),
        ('driver', False),
        ('user', True),
        ('password', True),
        ('host', True),
        ('port', True),
        ('db', True),
        ('options', False),
    )

    conf = {}
    for param, required in required_params:
        obj = db_conf.get(param, None)
        if required and obj is None:
            raise DBAggregatorException('param: "{}" not found'.format(param))
        conf[param] = obj or ''

    conf['dialect'] = str(conf['dialect']).lower()
    if conf['dialect'] not in ('mysql', 'postgresql'):
        raise DBAggregatorException('dialect: "{}" not supported'.format(conf['dialect']))

    conf['port'] = ':{}'.format(conf['port']) if conf.get('port') else ''
    conf['driver'] = '+{}'.format(conf['driver']) if conf.get('driver') else ''

    conn_string = '{dialect}{driver}://{user}:{password}@{host}{port}/{db}{options}'.format(**conf)

    return conn_string


def conn_str_by_iniconf(iniconf_list, sections=None):
    config_parser = SafeConfigParser()
    config_parser.read(iniconf_list)

    result = {}
    for section in config_parser.sections():

        if sections is not None and section not in sections:
            continue

        conn_string = conn_str_by_dict(dict(config_parser.items(section)))
        result[section] = conn_string

    return result


def aggregate_by_iniconf(iniconf_list, sections=None, db_aggregator=None, engine_args=None):
    db = db_aggregator or DBAggregator()

    for session, conn_string in conn_str_by_iniconf(iniconf_list, sections).iteritems():
        db.add(session, conn_string, engine_args)

    return db
