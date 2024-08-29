# json netlist to dot
import os
import sys
# 获取当前执行文件 (__file__) 的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取当前文件所在目录的父目录
parent_dir = os.path.dirname(os.path.dirname(current_file_path))
# 将父目录添加到 Python 路径中
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import argparse
from base.xpnr import Context
from frontend.json_frontend import parse_json
from export.pydot import write_dot

def main():
    pass
    parser = argparse.ArgumentParser(description="Xilinx Place and Route")
    parser.add_argument("json", type=str, help="input json file")
    parser.add_argument("dot", type=str, help="output dot file")

    args = parser.parse_args()
    ctx = Context()
    ctx.set_args(args)
    parse_json(ctx, ctx.args.json)
    write_dot(ctx, ctx.args.dot)
    pass

if __name__ == "__main__":
    main()


        
