# coding: utf8
from setuptools import setup

with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

setup(
    name='dbaggregator',
    version='0.1',
    description='Package helpful to manage database connections',
    url='https://github.com/luivilella/db-aggregator',
    author='Luis Eduardo Vilella',
    author_email='luivilella@gmail.com',
    license='BSD',
    install_requires=requirements,
    zip_safe=False,
)
