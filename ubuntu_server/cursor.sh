#一旦xcompmgr &
sleep 1
# xwinwrapで透明ウィンドウを最前面表示・マウス透過
#xwinwrap -g 1024x768+0+0 -ni -argb -fs -fdt -un -b -nf -- python fake_cursor.py &

export DISPLAY=:1

# fake_cursor.py をバックグラウンドで起動し、PIDを保存
python fake_cursor.py &
echo $! > /tmp/fake_cursor.pid

# フォアグラウンドで動かす（SIGINTに反応するように）
wait
