
import os
import sys

from .env import ROSVenv, EnvNotFound, EnvAlreadyExist

name = 'init'
desc = 'Initialize the current directory with a ROS virtual environment.'

def prepare_arguments(parser):
    parser.add_argument('--distro', type=str,
            default=os.environ.get('ROS_DISTRO', default='melodic'),
            help='ROS distro')
    parser.add_argument('-b', '--build', action='store_true', default=False,
            help='build user base image if it does not exist')
    parser.add_argument('--all', action='store_true', default=False,
            help='add all directories to the mount list')
    parser.add_argument('--dir', type=str, action='append',
            help='add DIR to mount the mount list')

    return parser


def run(args):
    try:
        return _init(args)
    except EnvAlreadyExist as e:
        print(e)
    return 1


def _init(args):

    cwd = os.getcwd()
    env = ROSVenv()

    # Possible mounts
    mounts = [x for x in os.listdir(cwd)]
    if not args.all:
        # The argument --all was not used.
        # Hence, only the directories added with --dir will go to the mount list.
        # The directory must exist to be a valid mount point
        mounts = list(set(args.dir or []) & set(mounts))

    env.signify(cwd, args.distro, mounts)
    env.attach(cwd)

    env.print()

    if not env.env_base_exists:
        build = args.build

        if not build:
            print('Base user image does not exist, build it now? [y/N]', end=' ')
            choice = input().lower()
            if choice and choice[0] == 'y':
                build = True

        if build:
            print(f'Building base, please wait...', end=' ', flush=True)
            ok = env.build_base()
            if ok:
                print('[DONE]')
            else:
                print('[FAIL]')

        else:
            print('WARNING: user base image not built, use `vre run` to trigger a build.')

    return 0

