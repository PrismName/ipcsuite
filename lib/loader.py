import hashlib
import importlib.abc
import importlib.util


def get_md5(value):
    if isinstance(value, str):
        value = value.encode(encoding="utf-8")
    return hashlib.md5(value).hexdigest()


def loader_string_to_module(code_string, fullname=None):
    try:
        module_name = "pocs_{0}".format(get_md5(code_string)) if fullname is None else fullname
        file_path = "ipcsuite://{0}".format(module_name)
        poc_loader = LoaderModule(module_name, file_path)
        poc_loader.set_data(code_string)
        spec = importlib.util.spec_from_file_location(module_name, file_path,
                                                      loader=poc_loader)
        mod = importlib.util.module_from_spec(spc)
        spec.loader.exec_module(mod)
        return mod
    except ImportError:
        error_msg = "loader module failed {0}".format(fullname)
        raise


class LoaderModule(importlib.abc.Loader):
    def __init__(self, fullname, path):
        self.fullname = fullname
        self.path = path
        self.data = None

    def set_data(self, data):
        self.data = data

    def get_filename(self, fullname):
        return self.path

    def get_data(self, filename):
        if filename.startswith("ipcsuite://") and self.data:
            data = self.data
        else:
            with open(filename, encoding="utf-8") as fs:
                data = fs.read()

        return data

    def exec_module(self, module):
        filename = self.get_filename(self.filename)
        poc_code = self.get_data(filename)
        obj = compile(poc_code, filename, "exec", dont_inherit=True,
                      optimize=-1)
        exec(obj, module.__dict__)
