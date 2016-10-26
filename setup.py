from setuptools import setup

# to build - python setup.py sdist upload
setup(
    name='mangopaysdk',
    version='2.1.1',
    author='Mangopay (www.mangopay.com)',
    author_email='support@mangopay.com',
    packages=['mangopaysdk', 'mangopaysdk.entities', 'mangopaysdk.tools', 'mangopaysdk.tools.storages', 'mangopaysdk.types', 'mangopaysdk.types.exceptions'],
    url='https://pypi.python.org/pypi/mangopaysdk/',
    description='MANGOPAY API',
    long_description=open('README.md').read(),
    install_requires=[
        "requests>=2.4.3",
        "requests-oauthlib>=0.4.0",
        "fasteners>=0.14.1"
    ],
    keywords="emoney api sdk mangopay"
)
