#!/bin/bash
# start.sh：仮想GUI + VNC + noVNC + アプリの起動

export DISPLAY=:1
export XAUTHORITY=/root/.Xauthority  
touch /root/.Xauthority

# DISPLAY=:1 にアクセスできるように許可（root→X）
xhost +SI:localuser:root

# 1. 仮想Xサーバ起動（バックグラウンド）
Xvfb :1 -screen 0 1024x768x16 &
sleep 1

xauth generate :1 . trusted

# 2. 軽量デスクトップ起動
xfce4-session &

# 3. VNCサーバ起動（パスワードなし）
x11vnc -display :1 -nopw -forever -shared -cursor arrow -noxdamage &

# 4. noVNCサーバ起動（Web UIは http://localhost:6080）
/opt/websockify/websockify-master/run --web=/opt/novnc 6080 localhost:5900 &

# Firefoxをバックグラウンドで起動
sleep 5
firefox-esr &

#↓わんちゃん必要->irann
#xterm -geometry 40x5+800+0 -e watch -n 0.1 "xdotool getmouselocation" &

# マウスカーソルテーマとサイズを変更（大きく目立たせる）
# GTKベースの環境で効果が出る場合が多い

#killall unclutter
#gsettings set org.gnome.desktop.interface cursor-theme 'ComixCursors-Opaque-White'
#gsettings set org.gnome.desktop.interface cursor-size 48


#mouse poiter
#xcompmgr &

# 5. Python受信サーバを起動（Ubuntu側のメインアプリ）
python receiver.py


#実行に必要：chmod +x ubuntu_server/start.sh



# カレントディレクトリは HandGesturePCControl/
#cd ubuntu_server
# Dockerビルド（やや時間かかります）(dockerfile書き直したりしたらまた実行)
#docker build -t handgesture-novnc .
# X11不要！ブラウザでGUI表示 → 起動
#docker run --rm -it -p 127.0.0.1:6080:6080 -p 127.0.0.1:7777:8888 handgesture-novnc
#一度作ったらあとは以下で再スタートできる
#docker ps -a
#docker start -ai <bold_fermi>
#http://localhost:6080/

#ストレージ関連
#docker system df
#docker builder prune


#-i = --interactive
#標準入力（キーボード入力）を有効にして、コンテナにコマンドを送れるようにします。
#-t = --tty
#コンテナに 疑似ターミナル を割り当てます。