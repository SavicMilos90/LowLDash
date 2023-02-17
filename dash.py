import os
import subprocess
import re
import sys
import shutil
import time
import argparse


parser=argparse.ArgumentParser()

parser.add_argument("--source", "-s", help="Source stream")
parser.add_argument("--target_dir", "-t", help="Target dir, master.mpd is hardcoded")
parser.add_argument("--idr", "-i", help="keyframes in seconds", type= int , default= 2)
parser.add_argument("--encoder", "-e" , help="Chose enkoder", default= "libx264")

args=parser.parse_args()



source = args.source
target_dir = args.target_dir
idr = str(args.idr)
encoder = args.encoder



ffmpeg = shutil.which('ffmpeg')
if not ffmpeg:
	raise Exception('ffmpeg is not installed')

	
def process_movie(source,target_dir,encoder,idr):

	if not os.path.exists(target_dir):
		os.makedirs(target_dir)

	cmd = "ffmpeg -flags +global_header -i '" + source + "' -filter_complex \"bwdif=0:0:0,settb=AVTB,setpts='trunc(PTS/1K)*1K+st(1,trunc(RTCTIME/1K))-1K*trunc(ld(1)/1K)',drawbox=x=0:y=0:width=400:height=100:color=black@0.5:t=fill,drawtext=text='%{localtime\:%H}\:%{localtime\:%M}\:%{localtime\:%S}.%{eif\:1M*t-1K*trunc(t*1K)\:d\:3}':x=15:y=20:fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:fontsize=80:fontcolor=white,split=3[s0][s1][s2];[s0]scale=1920x1080[s0];[s1]scale=1280x720[s1];[s2]scale=768x432[s2]\" -pix_fmt yuv420p -c:v "+encoder+" -b:v:0 3500K -minrate:v:0 3000K -maxrate:v:0 4500K -bufsize:v:0 8000K -b:v:1 2500K -minrate:v:1 2000K -maxrate:v:1 3000K -bufsize:v:1 6000K -b:v:2 1000K -minrate:v:2 800K -maxrate:v:2 1500K -bufsize:v:2 3000K  -sc_threshold:v 0 -force_key_frames 'expr:gte(t,n_forced*"+idr+")' -c:a aac -bf 2 -ar 48000 -b:a 128k -map [s0] -map [s1] -map [s2] -map 0:a:0 -preset veryfast -tune zerolatency -adaptation_sets 'id=0,seg_duration=2.000,streams=v id=1,seg_duration=2.000,streams=a' -use_timeline 0 -streaming 1 -window_size 2 -frag_type every_frame -ldash 1 -utc_timing_url 'http://time.akamai.com?iso&amp;ms' -format_options 'movflags=cmaf' -timeout 0.5 -write_prft 1 -target_latency '4.0' -http_persistent 1 -hls_playlist 1 -remove_at_exit 1 -init_seg_name init\$RepresentationID\$.\$ext\$ -media_seg_name chunk\$RepresentationID\$-\$Number%05d\$.\$ext\$ -f dash '"+target_dir+"master.mpd'"
	
	log_path = target_dir + "logs/";
	
	if not os.path.exists(log_path):
		os.makedirs(log_path)


	log_name = int(time.time()) 
	
	cmd += ' 2>> '+ log_path + '{}.log'.format(log_name)

	proc = subprocess.Popen(cmd, shell=True,  stdout=subprocess.PIPE, stdin=subprocess.PIPE)


process_movie(source,target_dir,encoder,idr)





