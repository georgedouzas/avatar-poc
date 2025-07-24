
# Setup environment
!sudo apt-get update
!apt install software-properties-common
!sudo apt-get install python3.8 python3.8-distutils
!curl -sS https://bootstrap.pypa.io/pip/3.8/get-pip.py -o get-pip.py
!sudo python3.8 get-pip.py
!python3.8 -m pip install -U setuptools wheel

# Install SadTalker and fetch data
!git clone https://github.com/cedro3/SadTalker.git &> /dev/null
%cd SadTalker
!export PYTHONPATH=/content/SadTalker:$PYTHONPATH
!python3.8 -m pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
!apt update
!apt install ffmpeg &> /dev/null
!python3.8 -m pip install -r requirements.txt
!rm -rf checkpoints
!bash scripts/download_models.sh
