#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name='poolctl',
    packages=find_packages(),
    version='0.0.1',
    description='To control the testing pool.',
    author='Taihsiang Ho (tai271828)',
    author_email='taihsiang.ho@canonical.com',
    url='https://github.com/tai271828/poolctl',
    download_url='https://github.com/tai271828/poolctl.git',
    keywords=['pool', 'sru'],
    entry_points={
        'console_scripts': [
            'pool-cli=poolctl.commands.pool_cli:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python",
    ]
)
