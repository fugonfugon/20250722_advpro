# Dockerfile：軽量GUI + noVNC付きのUbuntu環境
#http://localhost:6080/

FROM python:3.11-slim

# 環境変数（noVNCポートなど）
ENV DISPLAY=:1
ENV DEBIAN_FRONTEND=noninteractive

# パッケージ更新 + GUI/VNC/ツール最小限インストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    xfce4 xfce4-terminal \
    x11vnc xvfb x11-utils scrot \
    x11-xserver-utils \
    wget unzip curl net-tools \
    python3-tk python3-dev \
    libx11-dev libxtst6 libpng-dev libxrandr-dev libxss1 libxi6 x11-xserver-utils \
    dbus-x11 \
    xauth \
    git \
    firefox-esr \
    fonts-noto-cjk \
    fonts-ipafont-gothic \
    fonts-takao \
    iptables \
    xdotool wmctrl\
    scrot \
    libxtst6 \
    libxss1 \
    libxrandr2 \
    libxinerama1 \
    libxcomposite1 \
    libxi6 \
    libglib2.0-0 \
    xcompmgr libglu1-mesa freeglut3-dev \
    libgtk-3-dev \
    build-essential \
    libxext-dev \
    libxrender-dev \
    pkg-config \
    comixcursors \ 
    libxcomposite-dev libxdamage-dev libxrandr-dev libxss-dev \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# noVNC & websockify のセットアップ（gitではなくzip）
RUN mkdir -p /opt/websockify && \
    wget -qO /tmp/novnc.zip https://github.com/novnc/noVNC/archive/refs/heads/master.zip && \
    unzip /tmp/novnc.zip -d /opt/ && \
    mv /opt/noVNC-master /opt/novnc && \
    ln -s /opt/novnc/vnc_lite.html /opt/novnc/index.html && \
    wget -qO /tmp/websockify.zip https://github.com/novnc/websockify/archive/refs/heads/master.zip && \
    unzip /tmp/websockify.zip -d /opt/ && \
    mv /opt/websockify-master /opt/websockify && \
    rm /tmp/novnc.zip /tmp/websockify.zip && \
    cd /opt && \
    git clone https://github.com/ujjwal96/xwinwrap.git && \
    cd xwinwrap && \
    make && \
    cp xwinwrap /usr/local/bin/

# Pythonパッケージのインストール
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# コード配置
COPY . /app/
WORKDIR /app/

# 起動スクリプト実行（GUI + VNC + サーバ起動）
CMD ["bash", "start.sh"]
