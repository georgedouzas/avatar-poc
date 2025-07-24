# Setup environment
sudo apt-get update
apt install software-properties-common
sudo apt-get install python3.9 python3.9-distutils
curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3.9 get-pip.py
python3.9 -m pip install -U setuptools wheel

# Install piper and fetch data
python3.9 -m pip install piper-tts
python3.9 -m piper.download_voices en_US-lessac-medium
python3.9 -m piper.download_voices el_GR-rapunzelina-low
