from setuptools import setup

setup(
    name='metabase-mate',
    version='1.1.0',
    packages=['metabase_mate'],
    url='https://github.com/omkar1610/metabase_mate',
    author='Omkar Ashrit',
    author_email='omkar.ashrit@gmail.com',
    description='A Python module for working with Metabase',
    long_description='Mate is a Python utility module that automates repetitive tasks in the Metabase UI, saving time and effort. It provides functionality to edit existing questions by adding new linked filters and updating older filters. Additionally, Mate can replicate dashboards with linked filters and apply partner-specific or static conditions to each question within the dashboard.'
)