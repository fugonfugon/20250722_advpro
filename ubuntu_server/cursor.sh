#一旦xcompmgr &
sleep 1
# xwinwrapで透明ウィンドウを最前面表示・マウス透過
xwinwrap -g 1024x768+0+0 -ni -argb -fs -fdt -un -b -nf -- python fake_cursor01.py &
