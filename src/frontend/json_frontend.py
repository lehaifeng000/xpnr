# 读取json网表

import json
from base.xpnr import Context, NetInfo, PortInfo, PortType, CellInfo

def parse_json(filename, ctx: Context):
    with open(filename, 'r') as f:
        data:dict = json.load(f)
    data_modules = data['modules']
    top_module_name = None
    # 找到top
    for module_name, module in data_modules.items():
        attrs = module.get("attributes")
        if attrs:
            top_attr = attrs.get("top")
            if top_attr:
                is_top = int(top_attr,2) == 1
                if is_top:
                    ctx.set_top_module(module_name)
                    top_module_name = module_name
    
    # import module
    top_module = data_modules[top_module_name]
    # attr

    # netnames
    netnames = top_module["netnames"]
    bit_maps = {}
    for netname, netdata in netnames.items():
        bits = netdata["bits"]
        # 如果是vector，拆分成多个net存储
        for index, bit in enumerate(bits):
            assert(bit not in bit_maps.keys())
            new_net = NetInfo()
            new_net.bit = bit
            if len(bits)>1:
                new_net.name = netname + "["+str(index)+"]"
            else:
                new_net.name = netname
            bit_maps[bit] = new_net
            ctx.nets[new_net.name] = new_net
    
    # top ports
    for portname, portdata in top_module["ports"].items():
        bits = portdata["bits"]
        direction = portdata["direction"]
        # 如果是vector，拆分成多个net存储
        for index, bit in enumerate(bits):
            net = bit_maps[bit]
            new_port = PortInfo()
            if len(bits)>1:
                new_port.name = portname + "["+str(index)+"]"
            else:
                new_port.name = portname
            if direction == "input":
                new_port.type = PortType.PORT_IN
                net.driver = new_port
            elif direction == "output":
                new_port.type = PortType.PORT_OUT
                net.users.append(new_port)
            ctx.ports[new_port.name] = new_port
    
    # cells
    for cellname, celldata in top_module["cells"].items():
        new_cell = CellInfo()
        new_cell.name = cellname
        new_cell.type = celldata["type"]
        for k,v in celldata["attributes"].items():
            new_cell.attrs[k] = property(v)
        for k,v in celldata["parameters"].items():
            new_cell.params[k] = property(v)
        
        for portname, bits in celldata["connections"].items():
            direction = celldata["port_directions"][portname]
            for bindex, bit in enumerate(bits):
                if bit == "0":
                    pass
                    continue
                elif bit == "1":
                    pass
                    continue
                elif bit == "x":
                    continue
                net = bit_maps[bit]
                if len(bits) > 1:
                    new_port_name = portname+"["+str(bindex)+"]"
                else:
                    new_port_name = portname
                new_port = PortInfo()
                new_port.name = new_port_name
                if direction == "input":
                    new_port.type = PortType.PORT_IN
                    net.driver = new_port
                elif direction == "output":
                    new_port.type = PortType.PORT_OUT
                    net.users.append(new_port)
                new_cell.ports[new_port_name] = new_port

        ctx.cells[cellname] = new_cell
    
    pass
        

                



            


            
        

    
    