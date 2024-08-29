from enum import Enum
from io import StringIO
import os
import json

class NodeShape(Enum):
    box='box'## 矩形
    record='record'
    polygon = 'polygon'# 多边形
    ellipse = 'ellipse'# 椭圆
    circle = 'circle'# 圆形
    point = 'point'# 点
    egg = 'egg'# 蛋形
    triangle = 'triangle'# 三角形
    plaintext = 'plaintext'# 文本标签，不带边框
    plain = 'plain'# 与 plaintext 类似，但允许边连接到标签的中心
    diamond = 'diamond'# 菱形
    trapezium = 'trapezium'# 梯形
    parallelogram = 'parallelogram'# 平行四边形
    house = 'house'# 房屋形状 (五边形)
    pentagon = 'pentagon'# 五边形
    hexagon = 'hexagon'# 六边形
    septagon = 'septagon'# 七边形
    octagon = 'octagon'# 八边形
    doublecircle = 'doublecircle'# 双圆
    doubleoctagon = 'doubleoctagon'# 双八边形
    tripleoctagon = 'tripleoctagon'# 三重八边形
    invtriangle = 'invtriangle'# 倒三角形
    invtrapezium = 'invtrapezium'# 倒梯形
    invhouse = 'invhouse'# 倒房屋形状
    Mdiamond = 'Mdiamond'# 带有圆角的菱形
    Msquare = 'Msquare'# 带有圆角的正方形
    Mcircle = 'Mcircle'# 双圆，内圆较小# 矩形

class PortType(Enum):
    IN=0
    OUT=1


class Port:
    def __init__(self, name="", ref_name="", parent_node=None, type = PortType.IN) -> None:
        self.parent_node = parent_node
        self.name = name
        self.ref_name = ref_name
        self.type = type
        pass

class Node:
    def __init__(self, name ="", bel_name=None, bel_type=None, shape =NodeShape.record, color="black", fontcolor="black" ) -> None:
        self.name = name
        self.bel_name = bel_name
        self.bel_type = bel_type
        # self.label = None
        self.shape = shape
        self.color = color
        self.fontcolor = fontcolor
        self.ports = {}
        self.ports_map = {}
        pass
    
    def add_port(self, name="",  type=PortType.IN):
        port_ref_name = "p"+str(len(self.ports)+1)
        self.ports[port_ref_name] =self.ports_map[name] = Port(name=name, ref_name=port_ref_name, type=type, parent_node=self)
        pass

    def get_port_by_name(self, port_name):
        return self.ports_map.get(port_name, None)
    
    def to_string(self):
        # 更新label
        if self.shape == NodeShape.record:
            self.label = "{{"
            # 输入port
            first = True
            for ind, (k, port) in enumerate(self.ports.items()):
                if port.type == PortType.IN:
                    if not first:
                        self.label+="|"
                    self.label+=f'<{k}> {port.name}'
                    first = False
            self.label+="}|{"
            self.label+=self.bel_name
            if self.bel_type != None:
                self.label+=f'|{self.bel_type}'
            self.label+="}|"
            # 输出port
            self.label+="{"
            first = True
            for ind, (k, port) in enumerate(self.ports.items()):
                if port.type == PortType.OUT:
                    if not first:
                        self.label+="|"
                    self.label+=f'<{k}> {port.name}'
                    first = False
            # label结束
            self.label+="}}"
        else:
            self.label = self.bel_name

        buf = f'{self.name} [ shape={self.shape.value}, label="{self.label}"'
        if self.color:
            buf+= f', color="{self.color}"'
        if self.fontcolor:
            buf+= f', fontcolor="{self.fontcolor}"'
        buf+="]"
        return buf
        
class Edge:
    def __init__(self, from_port, to_port, label="", color="black", fontcolor="black" ) -> None:
        pass
        self.from_port = from_port
        self.to_port = to_port
        self.label = label
        self.color = color
        self.fontcolor = fontcolor
    def to_string(self):
        # from_str = f'{self.from_port.parent_node.name}:{self.from_port.ref_name}:e
        if self.from_port.parent_node.shape == NodeShape.record:
            from_str = f'{self.from_port.parent_node.name}:{self.from_port.ref_name}:e'
        else:
            from_str = f'{self.from_port.parent_node.name}:e'

        if self.to_port.parent_node.shape == NodeShape.record:
            to_str = f'{self.to_port.parent_node.name}:{self.to_port.ref_name}:w'
        else:
            to_str = f'{self.to_port.parent_node.name}:w'

        buf = f'{from_str} -> {to_str} [ color="{self.color}",  fontcolor="{self.fontcolor}", label="{self.label}"]'
        return buf



class Graph:
    def __init__(self, name="top", label = "top", rankdir="LR", remincross="true") -> None:
        self.name = name
        self.label = label
        self.rankdir = rankdir
        self.remincross = remincross
        self.nodes = []
        self.edges = []
        self.tab = "    "
        self.node_bel_map = {}
    def add_node(self, node:Node):
        self.nodes.append(node)
        self.node_bel_map[node.bel_name] = node
    def get_node_by_bel_name(self,bel_name):
        return self.node_bel_map[bel_name]
    def add_edge(self, edge):
        self.edges.append(edge)
    
    def to_string(self):
        pass
        buffer = StringIO()
        # start
        buffer.write(f'digraph "{self.name}" {{{os.linesep}')
        buffer.write(f'{self.tab}label="{self.label}";{os.linesep}')
        buffer.write(f'{self.tab}rankdir="{self.rankdir}";{os.linesep}')
        buffer.write(f'{self.tab}remincross="{self.remincross}";{os.linesep}')

        # node
        for node in self.nodes:
            buffer.write(f'{self.tab}{node.to_string()};{os.linesep}')
        
        # edge
        for edge in self.edges:
            buffer.write(f'{self.tab}{edge.to_string()};{os.linesep}')

        # end
        buffer.write('}')
        return buffer.getvalue()

    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(self.to_string())
        
def write_dot(ctx, dot_file):
    graph = Graph()
    name_prefix = "n"
    if ctx.from_yosys:
        for port_name, top_port in ctx.ports.items():
            node = Node(name=name_prefix+str(len(graph.nodes)+1), bel_name=port_name, bel_type="PAD", shape=NodeShape.octagon)
            node.add_port(port_name, PortType.IN if top_port.type.value==0 else PortType.OUT)
            graph.add_node(node)

    for cell_name, cell in ctx.cells.items():
        node = Node(name=name_prefix+str(len(graph.nodes)+1), bel_name=cell_name, bel_type=cell.type)
        for port_name, port in cell.ports.items():
            node.add_port(port_name, PortType.IN if port.type.value==0 else PortType.OUT)
        graph.add_node(node)
    # edge
    for net_name, net in ctx.nets.items():
        if len(net.users)==0 or ((not net.constant) and net.driver is None):
            continue
        
        if net.constant:
            # 创建一个node
            if net.bit == '0':
                bel_type = "GND"
            elif net.bit == '1':
                bel_type = "VCC"
            else:
                bel_type = "X"
            node = Node(name=name_prefix+str(len(graph.nodes)+1), bel_name=net.bit, bel_type=bel_type, shape=NodeShape.octagon)
            node.add_port(net.name, PortType.IN)
            from_port = node.get_port_by_name(net.name)
            graph.add_node(node)
        else:
            if not net.driver.parent:
                continue
            from_node = graph.get_node_by_bel_name(net.driver.parent.name)
            from_port = from_node.get_port_by_name(net.driver.name)
        for user in net.users:
            if not user.parent:
                continue
            to_node = graph.get_node_by_bel_name(user.parent.name)
            to_port = to_node.get_port_by_name(user.name)
            # to_port = to_node.get_port_by_name(user.name+"_IO")
            edge = Edge(from_port=from_port, to_port=to_port)
            graph.add_edge(edge)
    with open(dot_file, 'w') as f:
        f.write(graph.to_string())
    print("end")










