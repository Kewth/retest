# from distutils.core import setup
from setuptools import setup
import os

plugins = ['plugin/' + i for i in os.listdir('plugin')]

setup(
    name='retest',
    version='1.0',
    author='Kewth',
    author_email='Kewth.K.D@outlook.com',
    description='retest for OIer',
    url='https://github.com/Kewth/retest',
    package_dir={'retest': 'source'},
    packages=['retest'],
    install_requires=[
        'argparse',
        'pyyaml',
        'colorama',
        'resource',
    ],
    data_files=[
        ('share/retest', ['spj', 'retest.yaml']),
        ('share/retest/plugin', plugins),
        ('bin', ['retest']),
    ],
    )
