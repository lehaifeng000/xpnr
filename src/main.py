import argparse
from base.xpnr import Context
from frontend.json_frontend import parse_json
from export.pydot import write_dot

def main():
    pass
    parser = argparse.ArgumentParser(description="Xilinx Place and Route")
    parser.add_argument("--json", type=str, help="input json file")

    args = parser.parse_args()
    ctx = Context()
    ctx.set_args(args)
    parse_json(ctx, ctx.args.json)
    write_dot(ctx, "t.dot")
    pass

if __name__ == "__main__":
    main()