""" Audio Display """
## Uses the MPV player to display useful information about incoming stereo audio
## Have a look here for a Windows download. https://github.com/Warblefly/MultimediaTools-mingw-w64

from string import Template
import argparse, tempfile, subprocess, json, pprint


def ffmpegEscape(input):
    return(input.replace("\\",  "\\\\").replace(":",  "\\:"))

## IMPORTANT -- CONFIGURATION ##
## PLEASE ENTER YOUR CONFIGURATION VALUES BELOW
##
##   The FULL PATH to your MPV binary
##   Please keep the 'r' at the front

#MPV = r"c:/Program Files/ffmpeg/bin/"

parser = argparse.ArgumentParser(description='Audio monitor. Requires one audio input.')
parser.add_argument('filename', metavar='file', help='Audio file to be displayed.')
parser.add_argument('-r', default=25, type=int, help='Frame rate to display.')
parser.add_argument('-j', action='store_true', help='Use Jack audio server')
parser.add_argument('-l', metavar='level', type=float, default=0.0, help='Input attenuation in dB')

args = parser.parse_args()
filename_raw = args.filename
rate = args.r
jack = args.j
level = args.l

filename = ffmpegEscape(filename_raw)


LAVFI = "[aid1]volume=" + str(-level) + "dB," + \
        "asplit=8[a][b][c][d][e][f][g][i];" + \
        "[a]avectorscope=size=360x360:zoom=0.1:swap=1:draw=line:rate=" + str(rate) + ",drawgrid=180:180:color=gray[z];" + \
        "[b]ebur128=video=1:meter=18[q][h];" + \
        "[q]fps=fps=" + str(rate) + ",scale=360:360[y];[z][y]hstack[w];" + \
        "[c]aresample=50000,showfreqs=fscale=lin:win_size=4096:cmode=separate:size=360x360,fps=fps=" + str(rate) + "," + \
        "drawgrid=x=0:y=0:w=90:h=180:color=gray[u];" + \
        "[d]showspectrum=overlap=1:slide=scroll:scale=5thrt:mode=combined:legend=1:fps=" + str(rate) + "," + \
        "scale=360:360[t];" + \
        "[t][u]hstack[v];" + \
        "[e]aresample=192000,volume=+5.2dB,showvolume=rate=" + str(rate) + ":w=720:h=40:t=0:f=0.9:v=1:m=p:dm=1:ds=lin," + \
        "drawtext=font=Arial:fontsize=16:" + \
	"text='1    2       3             4                      5                                   6                                                          7':" + \
	"x=35:y=34:fontcolor=white," + \
        "scale=720:-1[s];" + \
        "[f]showcqt=size=720x120:bar_g=7:bar_t=0.25:timeclamp=0.5:rate=" + str(rate) + "[r];" + \
        "[g]aphasemeter=size=720x39:rate=" + str(rate) + ":mpc=red[ao][p];" + \
        "[h]anullsink;" + \
        "[i]ahistogram=rate=" + str(rate) + ":size=720x80:rheight=1/2:acount=40:slide=scroll[x];" + \
        "[v][w][r][p][x][s]vstack=inputs=6,setsar=1/1[vo]"

if jack==True:
	jack_command = " --ao=jack --jack-name=Audiometer "
else:
	jack_command = " "


dos_command = 'mpv' + ' -v ' + jack_command + ' --lavfi-complex="' + LAVFI + '" ' + filename_raw

try:
    test = str(subprocess.check_output(dos_command, shell=True))
except subprocess.CalledProcessError as e:
    print(e)

    


