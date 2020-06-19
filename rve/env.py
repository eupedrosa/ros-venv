
import os
import re
import json
import copy
import docker
import hashlib

from os import path

from rve import PACKAGE_DIR

class EnvNotFound(Exception):
    pass

class EnvAlreadyExist(Exception):
    pass

class ROSVenv(object):

    SIG_FILE = 'ROSvenv'

    def __init__(self):
        self.id = None

    def signify(self, directory, distro, src_mounts, data_mounts):
        """ Create a signature file in the given directory.

        Parameters:
            directory (str): Put signature file in this directory.
            distro (str): ROS distro to use.
            src_mounts (list): List of directories to mount under ~/src.
            data_mounts (list): List of directories to mount under ~/data.

        Raises:
            EnvAlreadyExist: A signature file already exists.
        """
        if path.exists(directory) and path.isdir(directory):
            sig = path.join(directory, self.SIG_FILE)
            if path.exists(sig):
                raise EnvAlreadyExist('A virtual ROS environment already exists at this directory')

            with open(sig, 'w') as f:
                f.write(json.dumps({'distro': distro, 'src': src_mounts, 'data': data_mounts}, indent=4))

    def attach(self, maybe_root, force_distro=None):
        """ Find the environment root and get its properties.

        Parameters:
            maybe_root (str): Start the search here.
        """
        self.root = self._get_root(maybe_root)
        self.uid = os.getuid()
        self.gid = os.getgid()

        sigfile = path.join(self.root, self.SIG_FILE)
        with open(sigfile, 'r') as f:
            info = json.load(f)
            self.distro = info['distro'] if force_distro is None else force_distro
            self.src_mounts = info['src']
            self.data_mounts = info['data']

        salt = '{}:{}:{}:{}:'.format(self.distro, self.root, self.uid, self.gid)
        # salt with a list of all mounts
        mount = copy.copy(self.data_mounts)
        for k, v in self.src_mounts.items():
            mount.append(k)
            mount.extend(v)
        salt = salt + '|'.join(mount)

        safe_name = re.sub('[^a-zA-Z0-9_.-]', '_', os.path.basename(self.root))
        self.id = 're-' + safe_name + '-' + \
                hashlib.sha1(salt.encode('utf-8')).hexdigest()[:16]

        self.base_id = 'rvenv/{}/{}:{}'.format(self.uid, self.gid, self.distro)

        # Check thing on docker
        client = docker.from_env()

        # the base image exists?
        try:
            client.images.get(self.base_id)
            self.env_base_exists = True
        except docker.errors.NotFound:
            self.env_base_exists = False

        # the environment container exists?
        try:
            client.containers.get(self.id)
            self.env_container_exists = True
        except docker.errors.NotFound:
            self.env_container_exists = False

        client.close()

    def build_base(self):
        """Build base image for current user and distro.
        """

        if self.id is None:
            # TODO: Raise Error?
            return # Not attached to a valid environment

        if self.env_base_exists:
            return # Already exists

        buildargs = {'distro': self.distro, 'uid': str(self.uid), 'gid': str(self.gid)}
        buildpath = path.join(PACKAGE_DIR, 'data')

        client = docker.from_env()
        try:
            _, res = client.images.build(path=buildpath, tag=self.base_id,
                    rm=True, buildargs=buildargs)
        except docker.errors.BuildError:
            res = None

        client.close()
        return False if res is None else True

    def create_env(self):
        if self.id is None:
            # TODO: Raise Error?
            return # Not attached to a valid environment

        if not self.env_base_exists:
            # TODO:
            return # Cannot create env without base image

        DISPLAY = os.getenv('DISPLAY')
        # Generate authority file to acces X11
        xauth = '/tmp/.docker.xauth-' + str(self.uid)
        if not path.exists(xauth):
            os.system('touch ' + xauth)
            os.system(f"xauth nlist {DISPLAY} | sed -e 's/^..../ffff/' | xauth -f {xauth} nmerge -")

        client = docker.from_env()

        # Mounts for X11
        volumes = {}
        volumes['/tmp/.X11-unix'] = {'bind': '/tmp/.X11-unix', 'mode':'rw'}
        volumes[xauth] = {'bind': '/tmp/.docker.xauth', 'mode':'rw'}

        # source mounts
        homedir = f'/home/{self.distro}-dev/src'
        for k, v in self.src_mounts.items():
            for p in v:
                # By default all directories are mounted as read-only, unless
                # the directory ends with an '!'.
                if p[-1] == '!':
                    p = p[:-1]
                    mode = 'rw'
                else:
                    mode = 'ro'

                mpath = path.join(homedir, k, path.basename(p))
                volumes[path.abspath(p)] = {'bind': mpath, 'mode': mode}

        # data mounts
        homedir = f'/home/{self.distro}-dev/data'
        for p in self.data_mounts:
            # By default all directories are mounted as read-only, unless
            # the directory ends with an '!'.
            if p[-1] == '!':
                p = p[:-1]
                mode = 'rw'
            else:
                mode = 'ro'

            mpath = path.join(homedir, path.basename(p))
            volumes[path.abspath(p)] = {'bind': mpath, 'mode': mode}

        client.containers.create(self.base_id, devices=['/dev/dri/card0:/dev/dri/card0:rw'],
                hostname=self.id,
                environment={'DISPLAY': os.getenv('DISPLAY'), 'XAUTHORITY': '/tmp/.docker.xauth'},
                volumes=volumes, name=self.id, stdin_open=True, tty=True, privileged=True)

        client.close()
        self.env_container_exists = True

    def run_on_env(self, arguments):
        if self.id is None:
            # TODO: Raise Error?
            return # Not attached to a valid environment

        if not self.env_container_exists:
            # TODO:
            return # Cannot create env without base image

        client = docker.from_env()

        container = client.containers.get(self.id)
        if container.status != 'running':
            container.start()

        bake = ['docker', 'exec', '-w',
                f'/home/{self.distro}-dev', '-ti',
                self.id, '/ros_entrypoint.sh']

        if len(arguments) > 0:
            # Append `rosrun` to argumensts list if the first
            # argument starts with a '+'.
            if arguments[0][0] == '+':
                arguments[0] = arguments[0][1:]
                bake.append('rosrun')

            bake.extend(arguments)
        else:
            bake.append('bash')

        os.system(' '.join(bake))
        numproc = len(container.top()['Processes'])
        if numproc == 1:
            container.stop()

        client.close()

    def rm_env(self):
        if self.id is None:
            # TODO: Raise Error?
            return # Not attached to a valid environment

        if not self.env_container_exists:
            return # Nothing to do

        client = docker.from_env()
        container = client.containers.get(self.id)
        container.remove(force=True)
        client.close()

    def print(self):
        info = f'ROSvenv for "{self.distro}"'
        print(info)

    def _get_root(self, start_directory):
        """ Get the directory with the signature file.

        A root directory of the environment contains a signature file: 'VROSenv'.
        If the signature file is not found we search through the directory parents
        until a file is found. The search fails when it reaches the home directory
        of the user and a signature file is not found.

        Parameters:
            start_directory (str): Start the search here.

        Returns:
            str: The environment root directory.

        Raises:
            EnvNotFound: A signature file was not found, hence ans environment was
            not found.
        """
        home = path.expanduser('~')
        curdir = path.abspath(start_directory)
        found = False
        while not found:
            query = path.join(curdir, self.SIG_FILE)
            found = path.exists(query) and path.isfile(query)
            if not found:
                curdir = os.path.dirname(curdir)
                if curdir == home or curdir == '/':
                    break

        if not found:
            raise EnvNotFound(f'Virtual ROS environment not found')

        return curdir


