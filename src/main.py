import argparse
from base.xpnr import Context
from frontend.json_frontend import parse_json

def main():
    pass
    parser = argparse.ArgumentParser(description="Xilinx Place and Route")
    parser.add_argument("--json", type=str, help="input json file")

    args = parser.parse_args()
    ctx = Context()
    ctx.set_args(args)
    parse_json(ctx.args.json,ctx)
    pass

if __name__ == "__main__":
    main()