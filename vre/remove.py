
import os
import sys

from .env import VROSenv, EnvNotFound

name = 'rm'
desc = 'Remove the virtual ROS environment.'

def prepare_arguments(parser):
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

    env.attach(cwd)
    sigfile = os.path.join(env.root, env.SIG_FILE)
    print(f'Removing "{sigfile}", continue? [y/N]:', end=' ')
    choice = input().lower()

    if choice and choice[0] == 'y':
        os.remove(os.path.join(env.root, env.SIG_FILE))
    else:
        print('Signature file NOT removed!')
        return

    # ==
    if env.env_container_exists:
        print(f'Removing container "{env.id}", continue? [y/N]:', end=' ')

        choice = input().lower()
        if choice and choice[0] == 'y':
            env.rm_env()
        else:
            print('Container NOT removed!')


