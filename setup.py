from distutils.core import setup

# to build - python setup.py sdist upload
setup(
    name='mangopaysdk',
    version='0.1.5',
    author='Mangopay (www.mangopay.com)',
    # author_email='example@example.com',
    packages=['mangopaysdk', 'mangopaysdk.entities', 'mangopaysdk.tools', 'mangopaysdk.types', 'mangopaysdk.types.exceptions'],
    url='http://pypi.python.org/pypi/mangopaysdk/',
    description='MangoPay API',
    long_description=open('README.md').read(),
    install_requires=[
        "requests>=1.2.0",
        "requests-oauthlib>=0.3.0",
    ],
	keywords="leetchi api sdk mangopay"
)