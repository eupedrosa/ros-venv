
import os
import sys

from colorama import Fore, Style

from rve.env import ROSVenv, EnvNotFound

name = 'remove'
desc = 'Remove the ROS virtual environment.'

def prepare_arguments(parser):
    parser.add_argument('--distro', type=str, help='overwrite the ROS distro.')
    parser.add_argument('-s', '--signature', action='store_true', default=False,
            help='also remove signature file')
    return parser


def run(args):
    try:
        return _init(args)
    except EnvNotFound as e:
        print(e)
    return 1


def _init(args):

    cwd = os.getcwd()
    env = ROSVenv()

    env.attach(cwd, args.distro)

    if env.env_container_exists:
        message = f'Removing container {Fore.RED}{Style.BRIGHT}{env.id}{Fore.RESET}{Style.NORMAL}'
        if args.signature:
            message += f' and {Fore.RED}{Style.BRIGHT}ROSenv'

        print(message)
        print(f'continue? [y/N]:', end=' ')

        choice = input().lower()
        if choice and choice[0] == 'y':
            env.rm_env()
            print(Fore.GREEN + 'Done')
        else:
            print(Fore.YELLOW + 'Canceled!')


