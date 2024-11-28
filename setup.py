from setuptools import setup, find_packages

setup(
    name='lasplit',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        lasplit=main:cli
    ''',
)
