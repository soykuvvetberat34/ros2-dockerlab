FROM osrf/ros:humble-desktop

ENV DEBIAN_FRONTEND=noninteractive \
    ROS_DOMAIN_ID=42 \
    QT_X11_NO_MITSHM=1

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-colcon-common-extensions \
        python3-pytest \
        ros-humble-turtlesim \
        ros-humble-ament-flake8 \
        ros-humble-ament-pep257 \
    && rm -rf /var/lib/apt/lists/*

# Her interaktif kabukta ROS ortamı ve (varsa) derlenmiş workspace yüklensin
RUN echo 'source /opt/ros/humble/setup.bash' >> /root/.bashrc \
 && echo '[ -f /ros2_ws/install/setup.bash ] && source /ros2_ws/install/setup.bash' >> /root/.bashrc

WORKDIR /ros2_ws

CMD ["sleep", "infinity"]
