from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='metabase-mate',
    version='4.0.0',
    packages=['metabase_mate'],
    url='https://github.com/omkar1610/metabase_mate',
    author='Omkar Ashrit',
    author_email='omkar.ashrit@gmail.com',
    description='A Python module for working with Metabase',
    long_description=long_description,
    long_description_content_type="text/markdown"
)