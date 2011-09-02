import pytest
from konira.exc    import KoniraNoSkip
from konira.runner import TestEnviron
from konira.util   import name_convertion
from konira.runner import Runner



def pytest_addoption(parser):
    """Add option to collect Konira test cases"""
    group = parser.getgroup('Konira DSL test cases')
    group.addoption('--konira', action='store_true', help='Collects Konira test cases')



def pytest_collect_file(path, parent):
    if parent.config.option.konira and path.basename.lower().startswith("case_"):
        return KoniraFile(path, parent)



class KoniraFile(pytest.File):
    def collect(self):
        konira_runner = Runner([self.fspath], {})
        classes = konira_runner.classes(self.fspath.strpath)

        for case in classes:

            # Initialize the test class
            suite = case()

            # check test environment setup
            environ = TestEnviron(suite)

            methods = self.methods(suite)
            if not methods: return

            # Are we skipping?
            if self.safe_skip_call(environ.set_skip_if):
                return

            # Set before all if any
            environ.set_before_all()

            for test in methods:
                yield KoniraItem(str(test), self, suite, test)

            # Set after all if any
            environ.set_after_all()


    def safe_skip_call(self, env_call):
        try:
            env_call()
            return True
        except KoniraNoSkip:
            return False
        except Exception:
            return False


    def methods(self, suite):
        return self._collect_methods(suite)


    def _collect_methods(self, module):
        invalid = ['_before_each', '_before_all', '_after_each', '_after_all']
        return [i for i in dir(module) if not i.startswith('_') and i not in invalid and i.startswith('it_')]



class KoniraItem(pytest.Item):


    def __init__(self, name, parent, case, spec):
        super(KoniraItem, self).__init__(name, parent)
        self.spec = spec
        self.case = case


    def runtest(self):
        # check test environment setup
        environ = TestEnviron(self.case)

        # Set before each if any
        environ.set_before_each()

        getattr(self.case, self.spec)()

        # Set after each if any
        environ.set_after_each()

    def reportinfo(self):
        describe = "describe %s" % name_convertion(self.case.__class__.__name__)
        it = name_convertion(self.name, capitalize=False)
        describe_and_it = "%s ==>> %s" % (describe, it)
        return self.fspath, 0, describe_and_it
