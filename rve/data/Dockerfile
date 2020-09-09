
ARG distro
FROM ros:${distro}

ARG distro
ARG uid
ARG gid

RUN apt-get update && apt-get install apt-utils -y && \
    apt-get install --no-install-recommends -y \
    sudo ros-${distro}-desktop vim bash-completion \
    && if [ "${distro}" = "noetic" ]; then apt-get install -y python3-osrf-pycommon python3-catkin-tools python3-pip; else \
    apt-get install -y python-catkin-tools python-pip; fi \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/${distro}-dev && \
    echo "${distro}-dev:x:${uid}:${gid}:Developer,,,:/home/${distro}-dev:/bin/bash" >> /etc/passwd && \
    echo "${distro}-dev:x:${gid}:" >> /etc/group && \
    echo "${distro}-dev ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${distro}-dev && \
    chmod 0440 /etc/sudoers.d/${distro}-dev && \
    chown ${uid}:${gid} -R /home/${distro}-dev && \
    mkdir -p /run/user/${uid} && \
    chown ${uid}:${gid} -R /run/user/${uid}

COPY bashrc /home/${distro}-dev/.bashrc
COPY ros_entrypoint.sh /ros_entrypoint.sh

RUN chown ${uid}:${gid} /home/${distro}-dev/.bashrc

USER ${distro}-dev
ENV HOME /home/${distro}-dev
ENV XDG_RUNTIME_DIR /run/user/${uid}
ENV QT_X11_NO_MITSHM 1
ENV TERM xterm-color
