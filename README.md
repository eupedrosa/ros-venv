ROS Virtual Environment
==================================

Developed and maintained by Eurico Pedrosa

## Overview

This project provides a command line tool to facilitate the use of different [ROS][1] environments using docker.
With this tool you can run a complete [ROS][1] environment, including GUI applications with hardware acceleration (for now only Intel cards).

## Install

You can install by source
```bash
git clone https://github.com/eupedrosa/ros-venv
cd ros-venv
python3 setup.py install
```

## Quick start

After installation the command `rosh` should be available.
Run `rosh --help` for information about the available commands.

#### Create an environment
Run `rosh init` at the root of your workspace.
It will create a `ROSvenv` file that marks the current directory as the ROS environment root directory.

Use multiple `--src` to mount directories under the `src` directory in the ROS environment,
and multiple `--data` to mount directories under the `data` directory in the ROS environment,

Example:
```sh
rosh init --src my-awsome-code --data write-here!
```
Here `my-awsome-code` will be mounter under `src/my-awsome-code` with *read-only* properties and
`write-here` will be mounter under `data/write-here` with *read-write* properties.

#### Step into the virtual environment
Run `rosh run` in the environment root path, or any of its child directories, to launch a bash shell inside the virtual environment.

#### Quickly launch a program
You can, for example, run `rosh run roscore` to launch a `roscore` without stepping into a shell first.
Try `rosh run roscore` in one shell and `rosh run rviz` in another to verify that GL applications are working.


## Credits
This project is inspired by [docker-ros-box](https://github.com/pierrekilly/docker-ros-box).

[1]: http://wiki.ros.org
