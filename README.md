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

After installation the command `re` (short for ros-environment) should be available.
Run `re --help` for information about the available commands.

#### Create an environment
Run `re init` at the root of your workspace.
Use multiple `--dir` to add child directories to mount on the the environment container, or `--all` to include all child directories.
It will create a `ROSvenv` file that marks the current directory as the virtual ROS environment root directory.

#### Step into the virtual environment
Run `re run` in the environment root path, or any of its child directories, to launch a bash shell inside the virtual environment.

#### Quickly launch a program
You can, for example, run `re run roscore` to launch a `roscore` without stepping into a shell first.
Try `re run roscore` in one shell and `re run rviz` in another to verify that GL applications are working.


## Credits
This project is inspired by [docker-ros-box](https://github.com/pierrekilly/docker-ros-box).

[1]: http://wiki.ros.org
