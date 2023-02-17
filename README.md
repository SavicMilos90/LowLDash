# LowLDash

##Requriments : 

1.FFMPEG >5 
Instalation : 
sudo add-apt-repository ppa:savoury1/ffmpeg4
sudo add-apt-repository ppa:savoury1/ffmpeg5
sudo apt update
apt install ffmpeg
Tested on ubuntu 18 and 20

2.Python3

##Usage :

python3 dash.py -s <source> -t <target_dir> "optional parametars" -i <keyframes in seconds,default 2> -e <encoder,default libx264>

#NOTE: master.mpd is hardcoded in script so only path where chunks will be stored should be provider in -t parametar   