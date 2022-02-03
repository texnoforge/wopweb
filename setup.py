import setuptools


# get version
exec(open('wopweb/__init__.py').read())


setuptools.setup(
    version=__version__)
