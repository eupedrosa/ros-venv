#!/bin/bash
set -e

# setup ros environment
source "/opt/ros/$ROS_DISTRO/setup.bash"

if [[ -f "$HOME/devel/setup.bash" ]]; then
    source "$HOME/devel/setup.bash"

elif [[ -f "$HOME/devel_isolated/setup.bash" ]]; then
    source "$HOME/devel_isolated/setup.bash"

elif [[ -f "$HOME/install/local_setup.bash" ]]; then
    source "$HOME/install/local_setup.bash"
fi

exec "$@"
