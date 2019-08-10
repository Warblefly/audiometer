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

MPV = r"c:/Program Files/ffmpeg/bin/"

parser = argparse.ArgumentParser(description='Audio monitor. Requires one audio input.')
parser.add_argument('filename', metavar='file', help='Audio file to be displayed.')
parser.add_argument('-r', default=50, type=int, help='Frame rate to display.')

args = parser.parse_args()
filename_raw = args.filename
rate = args.r

filename = ffmpegEscape(filename_raw)


LAVFI = "[aid1]asplit=8[a][b][c][d][e][f][g][i];" + \
        "[a]avectorscope=size=360x360:zoom=0.1:swap=1:draw=line:rate=" + str(rate) + ",drawgrid=180:180:color=gray[z];" + \
        "[b]ebur128=video=1:meter=18[q][ao];" + \
        "[q]scale=360:360[y];[z][y]hstack[w];" + \
        "[c]showfreqs=fscale=lin:win_size=4096:cmode=separate:size=360x360," + \
        "drawgrid=x=0:y=0:w=90:h=180:color=gray,fps=fps=" + str(rate) + "[u];" + \
        "[d]showspectrum=overlap=1:slide=scroll:scale=5thrt:mode=combined:legend=1:fps=" + str(rate) + "," + \
        "scale=360:360:lanczos[t];" + \
        "[t][u]hstack[v];" + \
        "[e]showvolume=rate=" + str(rate) + ":w=720:h=40:t=0:f=0.9:dm=1," + \
        "drawtext=font=Arial:fontsize=16:text='1':x=35:y=34:fontcolor=white," + \
        "drawtext=font=Arial:fontsize=16:text='2':x=58:y=34:fontcolor=white," + \
        "drawtext=font=Arial:fontsize=16:text='3':x=96:y=34:fontcolor=white," + \
        "drawtext=font=Arial:fontsize=16:text='4':x=155:y=34:fontcolor=cyan," + \
        "drawtext=font=Arial:fontsize=16:text='5':x=248:y=34:fontcolor=white," + \
        "drawtext=font=Arial:fontsize=16:text='6':x=396:y=34:fontcolor=red," + \
        "drawtext=font=Arial:fontsize=16:text='7':x=631:y=34:fontcolor=pink," + \
        "scale=720:-1[s];" + \
        "[f]showcqt=size=720x120:bar_g=7:bar_t=0.25:timeclamp=0.5:rate=" + str(rate/2) + "[r];" + \
        "[g]aphasemeter=size=720x39:rate=" + str(rate/2) + ":mpc=red[h][p];" + \
        "[h]anullsink;" + \
        "[i]ahistogram=rate=" + str(rate) + ":size=720x80:rheight=1/2:acount=40:slide=scroll[x];" + \
        "[v][w][r][p][x][s]vstack=inputs=6,setsar=1/1[vo]"

dos_command = MPV + 'mpv.exe' + ' -v ' + ' --lavfi-complex "' + LAVFI + '" ' + filename_raw

try:
    test = str(subprocess.check_output(dos_command, stderr=subprocess.STDOUT)).split('\\n')
except subprocess.CalledProcessError as e:
    print(e)

    


