exec >/root/startup.log 2>&1
apt update
apt install -y python3-pip cython3
apt remove -y gnome-desktop3-data gnome-shell x11-xserver-utils libsnapd-glib1
apt remove -y gnome-session-common gnome-shell-common
pip3 install tensorflow
cd /tmp
wget https://xs.jdw.sx/files/cudnn-11.0-linux-x64-v8.0.5.39.tgz
tar -xvf cudnn-11.0-linux-x64-v8.0.5.39.tgz
mv cuda/lib64/* /usr/lib/.
echo "All set!"

