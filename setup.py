from distutils.core import setup

# to build - python setup.py sdist upload
setup(
    name='mangopaysdk',
    version='0.2.0',
    author='Mangopay (www.mangopay.com)',
    author_email='it-support@mangopay.com',
    packages=['mangopaysdk', 'mangopaysdk.entities', 'mangopaysdk.tools', 'mangopaysdk.tools.storages', 'mangopaysdk.types', 'mangopaysdk.types.exceptions'],
    url='http://pypi.python.org/pypi/mangopaysdk/',
    description='MangoPay API',
    long_description=open('README.md').read(),
    install_requires=[
        "requests>=1.2.0",
        "requests-oauthlib>=0.3.0",
        "lockfile>=0.9.1"
    ],
	keywords="leetchi api sdk mangopay"
)