"""
    A simple Minecraft NBT parser
    
    Specification: https://web.archive.org/web/20110723210920/http://www.minecraft.net/docs/NBT.txt
"""

import argparse
from NBTParser import Parser


def get_args_from_user() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        prog="NBTSnake",
        description="Minecraft NBT parser written in python"
    )
    
    arg_parser.add_argument("--file", "-f", help="Input file in .nbt format", required=True)
    arg_parser.add_argument("--output", "-o", help="Output file. JSON format", required=True)
    
    return arg_parser.parse_args()


def main():
    args = get_args_from_user()
    
    nbt_parser = Parser(args.file)

    nbt_parser.parse()
    
    nbt_parser.save_to_file(args.output)


if __name__ == '__main__':
    main()
