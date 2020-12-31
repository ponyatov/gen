import os,sys

class Object:
    def __init__(self,V):
        self.type = self.__class__.__name__.lower()
        self.value = V
        self.nest = []
    def __floordiv__(self,that):
        assert isinstance(that,Object)
        self.nest.append(that) ; return self
    def gen(self):
        for j in self.nest: j.gen()

class IO(Object): pass

class Dir(IO):
    def __floordiv__(self,that):
        assert isinstance(that,File)
        super().__floordiv__(that)
    def gen(self):
        try: os.mkdir(self.value)
        except FileExistsError: pass

class File(IO): pass

class Meta(Object): pass
class Module(Meta): pass

class mkFile(File):
    def __init__(self,V='Makefile'):
        super().__init__(V)

class dirModule(Module):
    def __init__(self,V=None):
        V = V if V else sys.argv[0].split('.')[0]
        super().__init__(V)
        self.d = Dir(V) ; self // self.d
        self.init_mk()

    def init_mk(self):
        self.d.mk = mkFile() ; self.d // self.d.mk

class pyModule(dirModule):
    def __init__(self,V=None):
        super().__init__(V)
        self.init_py()
    def init_py(self):
        pass

mod = pyModule()

mod.gen()
