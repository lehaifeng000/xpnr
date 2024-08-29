# 上下文，存网表、等各种信息

from enum import Enum


class Context:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Context, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, top_module_name=None) -> None:
        if not hasattr(self, 'initialized'):
            self.nets = {}
            self.cells = {}
            self.ports = {}
            self.settings = {}
            self.attrs = {}
            self.top_module_name = top_module_name
            self.initialized = True
            self.from_yosys = True
    def set_args(self,args):
        self.args = args
    def set_top_module(self,top_module_name):
        self.top_module_name = top_module_name
    def get_top_module(self):
        return self.top_module_name
    def write_json(self, filename):
        jsondata = {}
        jsondata["creator"] = "xilinx place and route by xpnr"
        topdata = {}
        topdata["settings"] = {}
        for k, v in self.settings.items():
            topdata["settings"][k] = v
        topdata["attributes"] = {}
        for k,v in self.attrs.items():
            topdata["attributes"][k] = v
        


class NetInfo:
    def __init__(self) -> None:
        pass
        self.name = None
        self.driver = None
        self.attrs = None
        self.wires = None
        self.users = []
        self.bit = None
        self.constant = False

class PortType(Enum):
    PORT_IN = 0
    PORT_OUT = 1
    PORT_INOUT = 2

class PortInfo:
    def __init__(self) -> None:
        pass
        self.name = None
        self.type = None
        self.parent = None
        self.is_top = False

class CellInfo:
    def __init__(self) -> None:
        pass
        self.name = None
        self.type = None
        self.ports = {}
        self.attrs = {}
        self.params = {}
        self.pins = {} # cell_port -> bel_pin
    def add_port(self, port):
        port.parent = self
        self.ports[port.name] = port


class Property:
    def is_number(self,s):
        allowed_chars = {'0', '1', 'x', 'z'}
        return all(char in allowed_chars for char in s)
    
    def __init__(self, str=None, num=None) -> None:
        if num is not None:
            self.is_num = True
            self.num = num
            self.str = str(num)
        elif str is not None:
            self.is_num = self.is_number(str)
            self.str = str
            if self.is_num:
                self.num = int(str, 2)
        pass

    def to_json(self):
        return self.str

if __name__ == "__main__":
    ctx1 = Context(top_module="top1")
    pass


