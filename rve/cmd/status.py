
import os
import sys
import argparse

import colorama
from colorama import Fore

from rve.env import ROSVenv, EnvNotFound

name = 'status'
desc = 'show virtual environment status.'

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
    env = ROSVenv()
    env.attach(cwd)

    base_status = Fore.GREEN + 'OK' if env.env_base_exists else Fore.RED + 'Missing'
    print("Base image: {}".format(base_status))

    if not env.env_container_exists:
        return

    print('Container')
    print('  name: ')



