
import sys
import argparse

import vre.init
import vre.remove
import vre.run

def _create_sub_parsers(parser):

    cmds = [vre.init, vre.remove, vre.run]
    cmds_names = [x.name for x in cmds]
    cmds_list = '[' + '|'.join(cmds_names) + ']'

    desc = 'call `vre command -h` for help in each command listed below:\n'
    for c in cmds:
        desc += f'\n {c.name}\t\t{c.desc}'

    subparser = parser.add_subparsers(
            title='vre command',
            metavar=cmds_list,
            description=desc,
            dest='cmd')

    for c in cmds:
        cmd_parser = subparser.add_parser(c.name,description=c.desc)
        cmd_parser = c.prepare_arguments(cmd_parser)
        cmd_parser.set_defaults(run=c.run)


def main():

    parser = argparse.ArgumentParser(description='vre command',
            formatter_class=argparse.RawDescriptionHelpFormatter)
    _create_sub_parsers(parser)
    args = parser.parse_args()

    if args.cmd is None:
        parser.print_help()
        sys.exit()

    sys.exit(args.run(args))
