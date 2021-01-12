


##  Install Python 3.8 with virtualenv
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.8
sudo apt install python3-venv virtualenv
virtualenv --python=/usr/bin/python3.8 venv



##  Install CUDA 11.0
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin
sudo mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/11.0.3/local_installers/cuda-repo-ubuntu1804-11-0-local_11.0.3-450.51.06-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1804-11-0-local_11.0.3-450.51.06-1_amd64.deb
sudo apt-key add /var/cuda-repo-ubuntu1804-11-0-local/7fa2af80.pub
sudo apt-get update
sudo apt-get -y install cuda

##  Install CuDNN
wget https://xs.jdw.sx/files/cudnn-11.0-linux-x64-v8.0.5.39.tgz
tar xvf cudnn-11.0-linux-x64-v8.0.5.39.tgz
sudo mv cuda/lib64/* /usr/lib/.

