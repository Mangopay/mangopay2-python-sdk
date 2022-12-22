from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mangopaysdk',
    version='3.24.0',
    description='A client library written in python to work with mangopay v2 api',
    long_description='This SDK is a client library for interacting with the Mangopay API.',
    url='https://github.com/Mangopay/mangopay2-python-sdk',
    author='Mangopay (www.mangopay.com)',
    author_email='support@mangopay.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='mangopay api development emoney sdk',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['requests', 'simplejson', 'blinker', 'six', 'pytz' ],
    extras_require={
        'dev': ['responses', 'nose', 'coverage', 'httplib2',
                'pyopenssl', 'ndg-httpsclient', 'pyasn1', 'exam'],
        'test': ['responses', 'nose', 'coverage', 'httplib2',
                 'pyopenssl', 'ndg-httpsclient', 'pyasn1', 'exam'],
    },
    entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    },
)
