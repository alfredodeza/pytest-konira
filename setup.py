from setuptools import setup

setup(
    name             = 'pytest-konira',
    description      = 'Run Konira DSL tests with py.test',
    author           = 'Alfredo Deza',
    author_email     = 'alfredodeza [at] gmail.com',
    version          = '0.1',
    license          = "MIT",
    keywords         = "test, readable, testrunner, bdd",
    py_modules       = ['pytest_konira'],
    entry_points     = {
        'pytest11': [
            'konira = pytest_konira',
        ]
    },
    install_requires = ['konira>=0.1.0', 'pytest>=2.0'],
    long_description = """

A Pytest Plugin for Konira test cases
-------------------------------------
This plugin allows you to collect and execute Konira test cases as you would
normally do with Konira's own test runner but with the extra functionality that
comes with the awesome py.test

Once the plugin is installed you get a single entry in the ``py.test`` help
menu giving you the option to add the ``--konira`` flag to collect cases.

Project page is at: http://github.com/alfredodeza/pytest-konira

The actual Konira project can be found at: http://konira.cafepais.com

"""
)
