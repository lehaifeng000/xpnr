# 读取json网表

import json
from base.xpnr import Context, NetInfo, PortInfo, PortType, CellInfo

def parse_json(ctx: Context, filename):
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

    # settings
    ctx.settings = top_module.get('settings',{})
    from_yosys = True
    if ctx.settings.get("synth", "0") != "0":
        from_yosys = False
        ctx.from_yosys = False

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
        # 如果是vector，拆分成多个net存储，由于写json时top port要保持原组合，保留组合信息
        for index, bit in enumerate(bits):
            net = bit_maps[bit]
            new_port = PortInfo()
            if from_yosys:
                new_port.parent = new_port
            new_port.is_top = True
            if len(bits)>1:
                new_port.name = portname + "["+str(index)+"]"
            else:
                new_port.name = portname
            if direction == "input":
                new_port.type = PortType.PORT_IN
                if from_yosys:
                    net.driver = new_port
            elif direction == "output":
                new_port.type = PortType.PORT_OUT
                if from_yosys:
                    net.users.append(new_port)
            ctx.ports[new_port.name] = new_port
    
    # cells
    for cellname, celldata in top_module["cells"].items():
        new_cell = CellInfo()
        new_cell.name = cellname
        new_cell.type = celldata["type"]

        if cellname == "$PACKER_VCC_DRV" or cellname == "$PACKER_GND_DRV":
            continue

        for k,v in celldata["attributes"].items():
            new_cell.attrs[k] = v
        for k,v in celldata["parameters"].items():
            new_cell.params[k] = v
        
        for portname, bits in celldata["connections"].items():
            if (not from_yosys) and new_cell.type == 'PAD': 
                port_type = PortType.PORT_OUT if new_cell.attrs["X_IO_DIR"] == "IN" else PortType.PORT_IN
            else:
                direction = celldata["port_directions"][portname]
            
            for bindex, bit in enumerate(bits):
                if bit == "0":
                    # 创建net
                    net = NetInfo()
                    net.name = cellname+"_"+portname+"_GND"
                    net.bit = "0"
                    net.constant = True
                    ctx.nets[net.name] = net
                elif bit == "1":
                    # 创建net
                    net = NetInfo()
                    net.name = cellname+"_"+portname+"_VCC"
                    net.bit = "1"
                    net.constant = True
                    ctx.nets[net.name] = net
                elif bit == "x":
                    continue
                else:
                    net = bit_maps[bit]

                if net.name == "$PACKER_GND_NET":
                    if direction == "output":
                        continue
                    # 绑定到0
                    net = NetInfo()
                    net.name = cellname+"_"+portname+"_GND"
                    net.bit = "0"
                    net.constant = True
                    ctx.nets[net.name] = net
                elif net.name == "$PACKER_VCC_NET":
                    if direction == "output":
                        continue
                    # 绑定到1
                    net = NetInfo()
                    net.name = cellname+"_"+portname+"_VCC"
                    net.bit = "1"
                    net.constant = True
                    ctx.nets[net.name] = net

                if len(bits) > 1:
                    new_port_name = portname+"["+str(bindex)+"]"
                else:
                    new_port_name = portname
                new_port = PortInfo()
                new_port.name = new_port_name
                if (not from_yosys) and new_cell.type == 'PAD':
                    new_port.type = port_type
                    if port_type == PortType.PORT_IN:
                        net.users.append(new_port)
                    else:
                        net.driver = new_port
                else:
                    if direction == "output":
                        new_port.type = PortType.PORT_OUT    
                        net.driver = new_port
                    elif direction == "input":
                        new_port.type = PortType.PORT_IN
                        net.users.append(new_port)
                    
                new_cell.add_port(new_port)

        ctx.cells[cellname] = new_cell
    
    pass
        
