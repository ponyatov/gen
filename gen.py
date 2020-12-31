import os,sys

class Object:
    def __init__(self,V):
        self.type = self.__class__.__name__.lower()
        self.value = V
        self.nest = []
    def __floordiv__(self,that):
        if isinstance(that,str): that = S(that)
        assert isinstance(that,Object)
        self.nest.append(that) ; return self
    def __format__(self,spec):
        assert not spec
        return self.head()
    def head(self,prefix=''):
        return f'{prefix}<{self.type}:{self.value}>'
    def gen(self,depth=0,to=None):
        ret = ''
        for j in self.nest: ret += j.gen(depth,to)
        return ret

class Primitive(Object): pass

class S(Primitive):
    def gen(self,depth=0,to=None):
        return f'{self.value}'

class Meta(Object): pass
class Module(Meta): pass

class Section(Meta):
    def gen(self,depth=0,to=None):
        assert isinstance(to,File)
        ret = ''
        if self.nest:
            ret += f'{to.comment} \\ {self}\n'
        for j in self.nest:
            ret += f'{j.gen(to)}\n'
        if self.nest:
            ret += f'{to.comment} / {self}\n'
        return ret

class IO(Object): pass

class File(IO):
    def __init__(self,V,comment='#'):
        super().__init__(V)
        self.comment = comment
        self.top = Section('top') ; self // self.top
        self.mid = Section('mid') ; self // self.mid
        self.bot = Section('bot') ; self // self.bot

    def gen(self,depth=0,to=None):
        assert isinstance(to,Dir)
        print(f'{self} {self.path}')
        with open(self.path,'w') as F:
            for j in self.nest:
                t = f'{j.gen(to=self)}'
                if t: F.write(f'{t}\n')

class gitiFile(File):
    def __init__(self,V='.gitignore',comment='#'):
        super().__init__(V,comment)
        self // f'!{self.value}'

class Dir(IO):
    def __init__(self,V):
        super().__init__(V)
        self.path = V
        self.giti = gitiFile() ; self // self.giti

    def __floordiv__(self,that):
        if isinstance(that,File):
            super().__floordiv__(that)
            that.path = f'{self.path}/{that.value}'
        elif isinstance(that,Dir):
            super().__floordiv__(that)
            that.path = f'{self.path}/{that.value}'
            that.giti.path = f'{that.path}/{that.giti.value}'
        else:
            raise TypeError(that)

    def gen(self,depth=0,to=None):
        try: os.mkdir(self.path)
        except FileExistsError: pass
        for j in self.nest: j.gen(to=self)

class mkFile(File):
    def __init__(self,V='Makefile'):
        super().__init__(V)

class dirModule(Module):
    def __init__(self,V=None):
        V = V if V else sys.argv[0].split('.')[0]
        super().__init__(V)
        self.d = Dir(V) ; self // self.d
        self.init_giti()
        self.init_mk()
        self.init_vscode()

    def gen(self,depth=0,to=None):
        self.d.gen(to=self)

    def init_giti(self):
        self.d.giti.top // '*~' // '*.log' // '*.log'

    def init_mk(self):
        self.d.mk = mkFile() ; self.d // self.d.mk
        self.d.mk.var = Section('var') ; self.d.mk // self.d.mk.var
        self.d.mk.var //\
            f'{"MODULE":<7}  = $(notdir $(CURDIR))' //\
            f'{"NOW":<7}  = $(shell date +%d%m%y)' //\
            f'{"REL":<7}  = $(shell git rev-parse --short=4 HEAD)'
        self.d.mk.tool = Section('tool') ; self.d.mk // self.d.mk.tool
        self.d.mk.tool //\
            f'{"WGET":<7}  = wget -c'

    def init_vscode(self):
        self.d.vscode = Dir('.vscode') ; self.d // self.d.vscode

class pyModule(dirModule):
    def __init__(self,V=None):
        super().__init__(V)
        self.init_py()
    def init_py(self):
        pass
    def init_mk(self):
        super().init_mk()
        self.d.mk.tool //\
            f'{"PY":<7}  = $(shell which python3)'

if __name__ == '__main__':
    if sys.argv[-1] == 'all':
        mod = pyModule()
        mod.gen()
