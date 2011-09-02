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
)
