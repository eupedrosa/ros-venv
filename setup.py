
import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "ros-venv",
    version = "0.0.1",
    install_requires=['docker==4.2.0', 'colorama=0.4.3'],
    author = "Eurico Pedrosa",
    author_email = "efp@ua.pt",
    description = ("Virtual ROS Environment is a tool to create isolated ROS environments."),
    license = "BSD",
    keywords = "ros-venv",
    url = "",
    packages=find_packages(),
    package_dir={'rve':'rve'},
    package_data={'rve': ['data/Dockerfile']},
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    entry_points={'console_scripts': ['rosh=rve.main:main']},
)
