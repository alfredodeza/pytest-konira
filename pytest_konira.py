import pytest
from konira.exc    import KoniraNoSkip
from konira.runner import TestEnviron
from konira.util   import name_convertion
from konira.runner import Runner


def pytest_collect_file(path, parent):
    if path.basename.startswith("case_"):
        return KoniraFile(path, parent)
            

class KoniraFile(pytest.File):
    def collect(self):
        konira_runner = Runner([self.fspath], {})
        classes = konira_runner.classes(self.fspath.strpath)

        for case in classes:
            name = name_convertion(case.__name__)
            yield KoniraItem(name, self, case)



class KoniraItem(pytest.Item):


    def __init__(self, name, parent, spec):
        super(KoniraItem, self).__init__(name, parent)
        self.spec = spec

    
    def runtest(self):
        # Initialize the test class
        suite = self.spec()

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

            # Set before each if any
            environ.set_before_each()

            getattr(suite, test)()
                
            # Set after each if any
            environ.set_after_each()

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


    def repr_failure(self, excinfo):
        """ called when self.runtest() raises an exception. """
        if isinstance(excinfo.value, BaseException):
            return "\n".join([
                "spec failed",
                "   %r" % excinfo.value.args
            ])


    def reportinfo(self):
        return self.fspath, 0, "konira case: %s" % self.name


    def methods(self, suite):
        return self._collect_methods(suite)


    def _collect_methods(self, module):
        invalid = ['_before_each', '_before_all', '_after_each', '_after_all']
        return [i for i in dir(module) if not i.startswith('_') and i not in invalid and i.startswith('it_')] 


