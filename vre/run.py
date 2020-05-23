
import os
import sys
import argparse

from .env import VROSenv, EnvNotFound

name = 'run'
desc = 'Execute the given command or swpan a shell.'

def prepare_arguments(parser):
    parser.add_argument('--distro', type=str, help='overwrite the ROS distro.')
    parser.add_argument('arguments', nargs=argparse.REMAINDER,
            help='run <arguments> in the environment container.')

    return parser


def run(args):
    try:
        return _init(args)
    except EnvNotFound as e:
        print(e)
    return 1


def _init(args):

    cwd = os.getcwd()
    env = VROSenv()

    env.attach(cwd, args.distro)

    if not env.env_base_exists:
        print('Base user image does not exist, build it now? [y/N]', end=' ')
        choice = input().lower()
        if choice and choice[0] == 'y':
            print(f'Building base, please wait...', end=' ', flush=True)
            ok = env.build_base()
            if ok:
                print('[DONE]')
            else:
                print('[FAIL]')
                sys.exit(1)

    if not env.env_container_exists:
        env.create_env()

    env.run_on_env(args.arguments)

