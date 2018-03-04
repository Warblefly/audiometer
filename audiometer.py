""" Audio Display """

from string import Template
import argparse, tempfile, subprocess, json, pprint


def ffmpegEscape(input):
    return(input.replace("\\",  "\\\\").replace(":",  "\\:"))

## IMPORTANT -- CONFIGURATION ##
## PLEASE ENTER YOUR CONFIGURATION VALUES BELOW
##
##   The FULL PATH to your FFmpeg binary
##   Please keep the 'r' at the front

MPV = r"c:/Program Files/ffmpeg/bin/"

##   The FULL PATHNAME of your font for the timecode

FONT = ffmpegEscape(r"c:/windows/fonts/arial.ttf")

parser = argparse.ArgumentParser(description='Audio monitor. Requires one audio input.')
parser.add_argument('filename', metavar='file', help='Audio file to be displayed.')

args = parser.parse_args()
filename_raw = args.filename

filename = ffmpegEscape(filename_raw)

LAVFI = "[aid1]asplit=7[a][b][c][d][e][f][g];" + \
        "[a]avectorscope=size=480x480:zoom=2:draw=line,drawgrid=240:240:color=gray[z];" + \
        "[b]ebur128=video=1:meter=18[q][ao];" + \
        "[q]scale=480:480[y];[z][y]hstack[w];" + \
        "[c]showfreqs=fscale=lin:win_size=w4096:cmode=separate:size=480x480:minamp=1e-009," + \
        "drawgrid=x=0:y=479:w=100:h=60:color=gray[u];" + \
        "[d]showspectrum=size=480x480:overlap=1:slide=scroll:scale=5thrt:mode=combined[t];" + \
        "[t][u]hstack[v];" + \
        "[e]showvolume=w=960:h=50:t=0:f=0.9," + \
        "drawtext=font=Arial:fontsize=24:text='1':x=47:y=40:fontcolor=white," + \
        "drawtext=font=Arial:fontsize=24:text='2':x=77:y=40:fontcolor=white," + \
        "drawtext=font=Arial:fontsize=24:text='3':x=128:y=40:fontcolor=white," + \
        "drawtext=font=Arial:fontsize=24:text='4':x=206:y=40:fontcolor=cyan," + \
        "drawtext=font=Arial:fontsize=24:text='5':x=330:y=40:fontcolor=white," + \
        "drawtext=font=Arial:fontsize=24:text='6':x=528:y=40:fontcolor=red," + \
        "drawtext=font=Arial:fontsize=24:text='7':x=842:y=40:fontcolor=pink[s];" + \
        "[f]showcqt=size=960x180:bar_g=7:timeclamp=0.5[r];" + \
        "[g]aphasemeter=size=960x40:mpc=red[h][p];" + \
        "[h]anullsink;" + \
        "[v][w][r][p][s]vstack=inputs=5,fps=50[vo]"

dos_command = MPV + 'mpv.exe' + ' -v ' + ' --lavfi-complex "' + LAVFI + '" ' + filename_raw

try:
    subprocess.check_output(dos_command, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as e:
    print(e)

    


