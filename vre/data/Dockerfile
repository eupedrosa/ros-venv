
ARG distro
FROM ros:${distro}

ARG distro
ARG uid
ARG gid

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    sudo ros-${distro}-desktop python-catkin-tools vim bash-completion \
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

USER ${distro}-dev
ENV HOME /home/${distro}-dev
ENV XDG_RUNTIME_DIR /run/user/${uid}
